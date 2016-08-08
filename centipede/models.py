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
import selenium
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
                    indent  = ('  ' * indent),
                    time    = time.strftime('%Y-%m-%d %H:%M:%S'),
                    message = msg,
                  )
            self._logger.write(log)

    ##
    # Funcitons for request

    def prepare_request(self, method, url, params, headers):
        r = requests.Request(
              method,
              url,
              params=params,
              headers=headers
            )
        return r.prepare()

    def send_request(self, method, url, params, headers):
        attempts = 0
        incr_delays = [1, 5, 10, 30, 60] # in minutes

        while True:
            try:
                response = self.session.send(
                             self.prepare_request(
                               method,
                               url,
                               params,
                               headers
                             ),
                             timeout = 30
                           )
                self.last_request = {'url': response.url, 'timestamp': time.time()}

                self._log(2,
                  '{url} ({time}s)'.format(
                    url  = response.url,
                    time = response.elapsed.total_seconds()
                  )
                )
                # TODO: Handle response status code, raise exceptions
            except requests.exceptions.RequestException as e:
                minutes = incr_delays[attempts]

                if attempts < 5:
                    self._log(0,
                      '[{errtype}] {msg}'.format(
                        msg     = str(e),
                        errtype = type(e).__name__,
                      )
                    )
                    self._log(0,
                      '[{errtype}] sleep {minutes} minutes..'.format(
                        errtype = type(e).__name__,
                        minutes = minutes,
                      )
                    )
                    time.sleep(minutes*60)
                    attempts += 1
                    continue
                else:
                    raise
                    # TODO: Handle complete abort
            else:
                break

        return response.url, response.content

    ##
    # Funcitons for main flow

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
                    j.module = self.load_module(module_name)
                    self.current_job = j

                    # print j.url, j.module

                    self._log(1,
                      'module: {module}, URL: {url}'.format(
                        url = url,
                        module = module_name,
                      )
                    )

                    return True

            except (JobError, ModuleError) as e:
                self._log(1,
                  '[{errtype}] {msg}'.format(
                    errtype = type(e).__name__,
                    msg = e.msg
                  )
                )
                continue

        self._log(1, 'No more jobs.')
        return False

    def do_job(self):
        self._log(1, 'Job started.')

        http_rules = self.current_job.module.http_rules
        part = 0
        root = None

        params  = http_rules.get('params', {})
        headers = {
          'User-Agent': self._user_agent,
          'Cache-Control': 'no-cache',
          'DNT': 1,
        }

        paging = None
        if 'page' in http_rules:
            paging_rules = http_rules['page']
            paging = Paging(
                      paging_rules.get('key', 'page'),
                      paging_rules.get('value', 1),
                      paging_rules.get('increment', 1)
                    )
            params[paging.key] = paging.page()

        data = list()
        while (not self.is_job_done(root)):
            url, html_source = self.send_request(
                                 http_rules.get('method', 'GET'),
                                 self.current_job.url,
                                 params,
                                 headers
                               )

            root = html.fromstring(html_source)

            data.extend(self.get_data(root))
            if len(data) >= 1000:
                self._log(1, 'Over 1k records, dumping the data.')

                if not part: part = 1

                self.dump_data(data, part)
                data = list()
                part += 1

            self.dump_new_jobs(root)

            # If page is defined, increase one. Continue until stop condition is matched
            if paging: params[paging.key] = paging.next_page()

            self.delay()

        self._log(1, 'Job done, dumping the data.')
        self.dump_data(data, part)
        return

    def close_job(self):
        with open(self.job_file, 'r+') as fp:
            jobs = fp.read().splitlines(True)
            fp.truncate(0)
            fp.seek(0)
            fp.writelines(jobs[1:])

        self._log(1, 'Job closed.')

    def run(self):
        self._log(0, 'Centipede starts!')
        self._log(0, 'Job filename: %s' % self.job_file)

        while (self.next_job()):
            self.do_job()
            self.close_job()

        self.close()

    def close(self):
        self._logger.close()

    def delay(self):
        diff = time.time() - self.last_request['timestamp']
        if (diff < self._delay):
            time.sleep(int(round((self._delay - diff), 0)))

    def load_module(self, module_name):
        module_fullname = 'centipede.module.' + module_name

        try:
            import importlib
            module = importlib.import_module(module_fullname)
        except ImportError as e:
            raise ModuleError(ModuleError.MODULE_NOT_FOUND, module_name)

        return module

    def dump_data(self, data, part=False):
        name = slugify_filename(self.current_job.url)

        if part:
            filename = '{name}.part{part}.json'.format(
                         name = name,
                         part = part,
                       )
        else:
            filename = '{name}.json'.format(name = name,)

        filepath = os.path.join(self._dir, filename)

        with open(filepath, 'w') as fout:
            json.dump(data, fout)

        self._log(1, "%d records are dumped to '%s'" % (len(data), filepath))

    def dump_new_jobs(self, root):
        if hasattr(self.current_job.module, 'new_jobs'):
            self._log(2, 'Adding new jobs:')

            jobs = list()
            for nj in self.current_job.module.new_jobs:
                for e in root.xpath(nj['path']):
                    url_prefix = nj.get('prefix', self.last_request['url'])
                    url = urlparse.urljoin(url_prefix, e.attrib['href'])

                    job = '{url}{delimiter}{module}\n'.format(
                            module    = nj['module'],
                            delimiter = '\t',
                            url       = url
                          )

                    jobs.append(job)

                    self._log(3,
                      'module: {module}, URL: {url}'.format(
                        url    = url,
                        module = nj['module'],
                      ),
                      indent=1
                    )

            with open(self.job_file, 'a+') as fout:
                fout.writelines(jobs)

            self._log(2, '%d new jobs are added.' % len(jobs))

    def get_data(self, root):
        elements = self.get_elements(root)
        self._log(2, '%d elements are found.' % len(elements))

        return self.get_elements_data(elements)

    def get_elements(self, root):
        return root.xpath(self.current_job.module.elements.get('path'))

    def get_elements_data(self, elements):
        self._log(3, 'Extracting data from elements:')

        module = self.current_job.module

        data = list()
        for e in elements:
            d = {}

            for key, info in module.elements['attributes'].iteritems():
                self._log(3,
                  '[{key}] info: {info}'.format(
                    key  = key,
                    info = str(info)
                  ),
                  indent=1
                )

                ee = e.xpath(info.get('path', '.'))
                if len(ee) == 0:
                    d[key] = self._null
                    continue

                if info.has_key('function'):
                    v = map(info['function'], ee)
                elif info.has_key('attrib'):
                    v = self.get_elements_data_from_attrib(ee, info['attrib'])
                else:
                    v = ee

                if info.has_key('regex') and all(isinstance(x, basestring) for x in v):

                    vv = list()
                    for x in v:
                        match = re.findall(info['regex'], x)

                        if match:
                            vv.append(match[0])
                        else:
                            vv.append(self._null)

                    v = vv

                d[key] = v

                self._log(3,
                  '[{key}] value: {value}'.format(
                    key   = key,
                    value = str(v)
                  ),
                  indent=1
                )

            # Add the timestamp
            d['timestamp'] = self.last_request['timestamp']

            data.append(d)

        return data

    def get_elements_data_from_attrib(self, elements, attrib):
        if attrib == 'text':
            return elements
        elif attrib == 'html':
            return map(etree.tostring, elements)
        else:
            return [e.attrib.get(attrib, self._null) for e in elements]

    def is_job_done(self, root):
        if root is None:
            return False
        else:
            condition = self.current_job \
                            .module \
                            .http_rules \
                            .get('stop', True)

            if isinstance(condition, dict):
                # TODO
                raise NotImplementedError()
            elif hasattr(condition, '__call__'):
                stop = condition(root)
            else:
                stop = True

            return stop


class Centipede_Selenium(Centipede):

    def __init__(self, fname, **kwargs):
        Centipede.__init__(self, fname, **kwargs)

        self.webdrive  = webdriver.Firefox()

    def send_request_by_selenium(self, url, params, headers):
        attempts = 0
        incr_delays = [1, 5, 10, 30, 60]

        while True:
            try:
                self.webdrive.get(
                  self.prepare_request(
                    'GET', 
                    url, 
                    params, 
                    headers
                  ).url
                )

                wait = ui.WebDriverWait(self.webdrive, 300)
                e = wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH,
                         self.current_job.module.http_rules['element'])
                         )
                    )
                
                self.last_request = {'url': self.webdrive.current_url, 'timestamp': time.time()}

            except selenium.common.exceptions.TimeoutException as e:
                print 'aaa'
                minutes = incr_delays[attempts]
                
                if attempts < 5:
                    self._log(0,
                      '[{errtype}] {msg}'.format(
                        msg     = str(e),
                        errtype = type(e).__name__,
                      )
                    )
                    self._log(0,
                      '[{errtype}] sleep {minutes} minutes..'.format(
                        errtype = type(e).__name__,
                        minutes = minutes,
                      )
                    )
                    time.sleep(minutes*60)
                    attempts += 1
                    continue
                else:
                    raise
            else:
                break

        return self.webdrive.current_url, self.webdrive.page_source

    def send_request_by_requests(self, method, url, params, headers):
        attempts = 0
        incr_delays = [1, 5, 10, 30, 60] # in minutes

        while True:
            try:
                response = self.session.send(
                             self.prepare_request(
                               method,
                               url,
                               params,
                               headers
                             ),
                             timeout = 30
                           )
                self.last_request = {'url': response.url, 'timestamp': time.time()}

                self._log(2,
                  '{url} ({time}s)'.format(
                    url  = response.url,
                    time = response.elapsed.total_seconds()
                  )
                )
                # TODO: Handle response status code, raise exceptions
            except requests.exceptions.RequestException as e:
                minutes = incr_delays[attempts]

                if attempts < 5:
                    self._log(0,
                      '[{errtype}] {msg}'.format(
                        msg     = str(e),
                        errtype = type(e).__name__,
                      )
                    )
                    self._log(0,
                      '[{errtype}] sleep {minutes} minutes..'.format(
                        errtype = type(e).__name__,
                        minutes = minutes,
                      )
                    )
                    time.sleep(minutes*60)
                    attempts += 1
                    continue
                else:
                    raise
                    # TODO: Handle complete abort
            else:
                break

        return response.url, response.content

    def send_request(self, method, url, params, headers):
        # if method.lower() == 'selenium':
            # return self.send_request_by_selenium(url, params, headers)
        # else:
            # return self.send_request_by_requests(method, url, params, headers)
        return self.send_request_by_selenium(url, params, headers)

class Paging(object):

    def __init__(self, key, start=1, increment=1):
        self.key = key
        self.current_page = start
        self.increment = increment

    def page(self):
        return self.current_page

    def next_page(self):
        self.current_page += self.increment
        return self.page()

    def prev_page(self):
        self.current_page -= self.increment
        return self.page()

