# -*- coding: utf-8 -*-

import requests
import os
import sys
import time
import re
import json
import urlparse
from lxml import html, etree

from .exceptions import JobError, ModuleError
from .job import CentipedeJob
from .utils import slugify_filename

from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Centipede:

    def __init__(self, fname, **kwargs):

        self._debug = False
        self._debug_level = 1

        self._log_level = 2
        self._logfile = None
        self._logs = list()
        self._logger = None

        self._dir = 'data'

        self._delay = 6
        self._last_request_time = 0
        self._last_request_url = None

        # Define the empty value for all column
        self._null = None

        self._user_agent = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'

        '''
        Check if a valid job queue is given.
        TODO: Make job queue can be given as a database connection.
        '''
        if not os.path.isfile(fname):
            raise JobError(JobError.FILE_NOT_FOUND, fname)

        self.job_file = fname

        '''
        Handle the kwargs.
        '''
        for k, v in kwargs.iteritems():
            if k == 'delay':
                self._delay = int(v)
            elif k == 'user_agent':
                self._user_agent = str(v)
            elif k == 'debug':
                self._debug = bool(v)
            elif k == 'debug_level':
                self._debug_level = int(v)
            elif k == 'log_level':
                self._log_level = int(v)
            elif k == 'dir':
                self._dir = str(v)
            elif k == 'logfile':
                self._logfile = str(v)
            else:
                continue    # just ignore the rest.

        '''
        Setup logging.
        '''
        if not self._logfile:
            self._logfile = os.path.join(sys.path[0], \
                              '{file}.{time}.log'.format(
                                file = self.job_file,
                                time = time.strftime('%Y%m%d%H%M%S')
                            ))

        self._logger = open(self._logfile, 'a+')

        '''
        Setup working ground.
        '''
        self._dir = os.path.join(sys.path[0], self._dir)

        if not os.path.exists(self._dir):
            os.makedirs(self._dir)

        '''
        Setup requests and selenium.
        '''
        self.session = requests.Session()

    def _log(self, level, msg, indent=0):
        if self._debug and self._debug_level >= level:
            print ('  ' * indent) + msg

        if self._log_level >= level:
            log = '{time}  {indent}{message}\n'.format(
                    indent = ('  ' * indent),
                    time = time.strftime('%Y-%m-%d %H:%M:%S'),
                    message = msg,
                  )
            self._logger.write(log)

            # self._logs.append(log)

        # if len(self._logs) >= 20:
            # self._dump_logs()

    def _dump_logs(self):
        with open(self._logfile, 'a+') as fout:
            fout.writelines(self._logs)

        del self._logs[:]

    def _prepare_request(self, method, params, headers):
        req  = requests.Request(
                 method,
                 self.current_job.url,
                 params=params,
                 headers=headers
               )
        return req.prepare()

    def _send_request(self, method, params, headers):
        attempts = 0
        delay_mins = [1, 5, 10, 30, 60]

        while True:
            try:
                res = self.session.send(
                        self._prepare_request(method, params, headers),
                        timeout = 30
                      )

                self._log(2, '{url} ({time}s)'.format(
                               url = res.url,
                               time = res.elapsed.total_seconds()
                             ))
                # TODO: Handle response status code, raise exceptions
            except requests.exceptions.RequestException as e:
                if attempts < 5:
                    self._log(1, '[{error_type}] {msg}'.format(
                                   error_type = type(e).__name__,
                                   msg = str(e),
                                 ))
                    self._log(1, '[{error_type}] sleep {mins} mins..'.format(
                                   error_type = type(e).__name__,
                                   mins = delay_mins[attempts]
                                 ))
                    time.sleep(delay_mins[attempts]*60)
                    attempts += 1
                    continue
                else:
                    raise
                    # TODO: Handle complete abort
            else:
                break

        return res.url, res.content

    def _delay_request(self):
        diff = time.time() - self._last_request_time
        if (diff < self._delay):
            time.sleep(int(round((self._delay - diff), 0)))

    def next_job(self):
        self._log(1, 'Finding next job.')

        with open(self.job_file, 'r') as fin:
            jobs = fin.read().splitlines()

        while jobs:
            job = jobs.pop(0)

            splits = job.strip().split("\t")

            try:
                if len(splits) < 2:
                    raise JobError(JobError.INVALID_FORMAT, job)
                else:
                    url, module_name = splits[-2:]
                    # print module_name, url

                    j = CentipedeJob()
                    j.url = url
                    j.module = self._load_module(module_name)

                    self.current_job = j

                    # print j.url, j.module

                    self._log(1, 'module: {module}, URL: {url}'.format(
                                   url = url,
                                   module = module_name,
                              ))

                    return True

            except (JobError, ModuleError) as e:
                self._log(1, '[{error_type}] {msg}'.format(
                               error_type = type(e).__name__,
                               msg = e.msg
                             ))
                continue

        self._log(1, 'No more jobs.')
        return False



    def do_job(self):
        self._log(1, 'Job started.')

        http_rules = self.current_job.module.http_rules
        stop = False

        headers = {
          'Cache-Control': 'no-cache',
          'User-Agent': self._user_agent,
          'DNT': 1,
        }
        params = http_rules.get('params', {})

        paging = http_rules.get('page')
        if paging:
            key = paging.get('key', 'page')
            val = paging.get('value', 1)
            params[key] = int(val)

        data = list()

        part = False
        while (not stop):
            url, html_source = self._send_request(
                                 http_rules.get('method', 'GET'),
                                 params,
                                 headers
                               )

            self._last_request_url  = url
            self._last_request_time = time.time()

            root = html.fromstring(html_source)

            data += self.get_data(root)

            if len(data) > 1000:
                self._log(1, 'Over 1,000 records, dumping the data.')

                if not part:
                    part = 1

                self.dump_data(data, part)
                data = list()
                part += 1


            self.dump_new_jobs(root)

            # If page is defined, increase one. Continue until stop condition is matched
            if paging:
                key = paging.get('key', 'page')
                params[key] += paging.get('increment', 1)

            stop = self._is_job_done(root)

            self._delay_request()

        self._log(1, 'Job done, dumping the data.')
        self.dump_data(data, part)
        return

    def close_job(self):
        with open(self.job_file, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(self.job_file, 'w') as fout:
            fout.writelines(data[1:])

        self._log(1, 'Job closed.')

    def _is_job_done(self, root):
        condition = self.current_job \
                        .module \
                        .http_rules \
                        .get('stop')

        if isinstance(condition, dict):
            # TODO
            raise NotImplementedError()
        elif hasattr(condition, '__call__'):
            stop = condition(root)
        else:
            stop = True

        return stop

    def run(self):
        self._log(0, 'Centipede starts!')
        self._log(0, 'Job filename: %s' % self.job_file)

        while (self.next_job()):
            self.do_job()
            # self.dump_new_jobs()
            self.close_job()
            # self.current_job = self.next_job()

        self.close()

    def close(self):
        # self._dump_logs()
        self._logger.close()
        pass

    def dump_data(self, data, part=False):
        name = slugify_filename(self.current_job.url)

        if part:
            fname = '{name}.part{part}.{ext}'.format(
                      part = part,
                      name = name,
                      ext  = 'json',
                    )
        else:
            fname = '{name}.{ext}'.format(
                      name = name,
                      ext  = 'json',
                    )

        fpath = os.path.join(self._dir, fname)

        with open(fpath, 'w') as fout:
            json.dump(data, fout)

        self._log(1, "%d records are dumped to '%s'" % (len(data), fpath))

    def dump_new_jobs(self, root):
        if hasattr(self.current_job.module, 'new_jobs'):
            self._log(2, 'Adding new jobs:')

            jobs = list()
            for nj in self.current_job.module.new_jobs:
                for e in root.xpath(nj['path']):
                    url = urlparse.urljoin(
                            nj.get('prefix', self._last_request_url),
                            e.attrib['href'],
                          )
                    job = '{url}{delimiter}{module}\n'.format(
                            module = nj['module'],
                            delimiter = '\t',
                            url = url,
                          )

                    jobs.append(job)

                    self._log(3,
                      'module: {module}, URL: {url}'.format(
                        url = url,
                        module = nj['module'],
                      ), indent=1)


            with open(self.job_file, 'a+') as fout:
                fout.writelines(jobs)

            self._log(2, '%d new jobs are added.' % len(jobs))

    def get_elements_attrib(self, elements, attrib):
        if attrib == 'text':
            return elements
            # v = [x.text for x in ee]
        elif attrib == 'html':
            return map(etree.tostring, elements)
        else:
            return [e.attrib.get(attrib, self._null) for e in elements]

    def get_elements_data(self, elements):
        self._log(3, 'Extracting data from elements:')

        module = self.current_job.module

        data = list()
        for e in elements:
            d = {}
            d['timestamp'] = self._last_request_time

            for key, info in module.elements['attributes'].iteritems():
                self._log(3, '[{key}] info: {info}'.format(
                               key = key,
                               info = str(info)
                             ), indent=1)

                ee = e.xpath(info.get('path', '.'))
                if len(ee) == 0:
                    d[key] = self._null
                    continue

                if info.has_key('function'):
                    v = map(info['function'], ee)
                elif info.has_key('attrib'):
                    v = self.get_elements_attrib(ee, info['attrib'])
                else:
                    v = ee

                if info.has_key('regex') and \
                   all(isinstance(x, basestring) for x in v):

                    t = list()
                    for x in v:
                        match = re.findall(info['regex'], x)

                        if match:
                            t.append(match[0] if match else None)
                        else:
                            t.append(self._null)

                    v = t

                # print v
                self._log(3, '[{key}] value: {value}'.format(
                               key = key,
                               value = str(v)
                             ), indent=1)

                d[key] = v

            data.append(d)

        return data

    def get_data(self, root):
        elements = root.xpath(self.current_job.module.elements['path'])
        self._log(2, '%d elements are found.' % len(elements))

        return self.get_elements_data(elements)

    def _load_module(self, module_name):
        try:
            import importlib
            m = importlib.import_module(
                  'centipede.module.{name}'.format(name=module_name)
                )

            # print m

        except ImportError as e:
            raise ModuleError(ModuleError.MODULE_NOT_FOUND, module_name)

        return m


class Centipede_Selenium(Centipede):

    def __init__(self, fname, **kwargs):
        Centipede.__init__(self, fname, **kwargs)

        self.webdrive  = webdriver.Firefox()

    def _send_request_by_selenium(self, params, headers):
        self.webdrive.get(self._prepare_request('GET', params, headers).url)

        wait = ui.WebDriverWait(self.webdrive, 3600)
        e = wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 self.current_job.module.http_rules['element'])
                 )
            )
        # TODO: Handle response status code, raise exceptions
        return self.webdrive.current_url, self.webdrive.page_source

    def _send_request_by_requests(self, method, params, headers):
        res  = self.session.send(self._prepare_request(
                                   method.upper(),
                                   params,
                                   headers
                                ))
        # TODO: Handle response status code, raise exceptions
        return res.url, res.content

    def _prepare_request(self, method, params, headers):
        req  = requests.Request(
                 method,
                 self.current_job.url,
                 params=params,
                 headers=headers
               )
        return req.prepare()

    def _send_request(self, method, params, headers):
        if method.lower() == 'selenium':
            return self._send_request_by_selenium(params, headers)
        else:
            return self._send_request_by_requests(method, params, headers)

