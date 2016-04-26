import requests
import os
import time
import re, json
from lxml import html, etree

class CentipedeJob:
    pass

class Error(Exception):
    pass

class JobError(Error):

    def __init__(self, msg):
        self.msg = msg

class ModuleError(Error):

    def __init__(self, msg):
        self.msg = msg

class Centipede:

    __user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/39.0.2171.95 Safari/537.36')
    __delay = 6
    __debug = False
    __debug_level = 1
    __log_level = 2
    __dir = 'centipede_data'

    def __init__(self, fname, **kwargs):

        '''
        Check if a valid job queue is given.
        TODO: Make job queue can be given as a database connection.
        '''
        if not os.path.isfile(fname):
            raise JobError('Job file not exists: \'%s\'' % fname)

        self.jobFile = fname

        '''
        Create log file for current job.
        '''
        if not os.path.exists('logs'):
            os.makedirs('logs')

        self.__log_file = 'logs/' + time.strftime('%Y%m%d%H%M%S') + '.log'
        self.__logs = list()
        self.__log(0, 'Job starts')
        self.__log(0, 'Job filename: %s' % self.jobFile)

        '''
        Handle the kwargs.
        '''
        for k, v in kwargs.iteritems():
            if k == 'delay':
                self.__delay = int(v)
            elif k == 'user_agent':
                self.__user_agent = str(v)
            elif k == 'debug':
                self.__debug = bool(v)
            elif k == 'debug_level':
                self.__debug_level = int(v)
            elif k == 'log_level':
                self.__log_level = int(v)
            elif k == 'dir':
                self.__dir = str(v)
            else:
                continue    # just ignore the rest.

        self.lastRequestTime = 0


    def __delay_request(self):
        diff = time.time() - self.lastRequestTime
        if (diff < self.__delay):
            time.sleep(int(round((self.__delay - diff), 0)))

    def __log(self, level, msg, indent=0):
        if self.__debug and self.__debug_level >= level:
            print msg

        if self.__debug_level >= level:
            log = ('    ' * indent) + time.strftime('%Y-%m-%d %H:%M:%S') + ' => ' + msg + '\n'
            self.__logs.append(log)
        
        if len(self.__logs) >= 20:
            self.__dump_log()
    
    def __dump_log(self):
        with open(self.__log_file, 'a+') as fout:
            fout.writelines(self.__logs)
        
        del self.__logs[:]

    def getJob(self):
        self.__log(1, 'Getting the next job.')

        try:
            with open(self.jobFile, 'r') as fin:
                data = fin.read().splitlines()

            if data:
                job = data[0]

                splits = job.rstrip().split("\t")
                if len(splits) != 2:
                    raise JobError('Incorrect job definition: \'%s\'' % job)
                else:
                    url, module = splits
                    # print module

                    j = CentipedeJob()
                    j.url = url
                    j.module = self.loadModule(module)

                    self.current_job = j
                    
                    self.__log(1, 'Module: %s, Url: %s' % (module, url))
                    return True
            else:
                self.__log(1, 'Job queue is empty.')
                return False
        except (JobError, ModuleError) as e:
            self.__log(1, type(e).__name__ + ': ' + e.msg)
            return False


    def doJob(self):
        self.__log(1, 'Job started.')

        stop = False
        
        params  = {}
        headers = {'User-Agent': self.__user_agent}
        
        if self.current_job.module.http_rules.has_key('page'):
            params[self.current_job.module.http_rules['page']['key']] = int(self.current_job.module.http_rules['page']['value'])

        if self.current_job.module.http_rules.has_key('pagesize'):
            params[self.current_job.module.http_rules['pagesize']['key']] = self.current_job.module.http_rules['pagesize']['value']

        if self.current_job.module.http_rules.has_key('params'):
            for k, v in self.current_job.module.http_rules['params'].iteritems():
                params[k] = v
        
        dlist = list()
        
        while (not stop):
            r = requests.get(self.current_job.url, params=params, headers=headers)
            root = html.fromstring(r.content)

            self.__log(2, r.url)
            self.lastRequestTime = time.time()

            dlist += self.extractData(root)
            self.dumpNewJobs(root)

            # If page is defined, increase one. Continue until stop condition is matched
            if self.current_job.module.http_rules.has_key('page'):
                params[self.current_job.module.http_rules['page']['key']] += 1

            # Stop condition must be a function, stop if not defined.
            if self.current_job.module.http_rules.has_key('stop'):
                f = self.current_job.module.http_rules['stop']
                if not hasattr(f, '__call__'):
                    raise ModuleError("Stop condition must be a function.")
                stop = f(root)
            else:
                stop = True

            self.__delay_request()

        self.dumpData(dlist)
        return

    def closeJob(self):
        with open(self.jobFile, 'r') as fin:
            data = fin.read().splitlines(True)
        with open(self.jobFile, 'w') as fout:
            fout.writelines(data[1:])

        self.__log(1, 'Job closed.')

    def run(self):
        while (self.getJob()):
            self.doJob()
            # self.dumpNewJobs()
            self.closeJob()
            # self.current_job = self.getJob()
        
        self.close()
    
    def close(self):
        self.__dump_log()

    def dumpData(self, dlist):
        self.__log(1, 'Job done, dumping the data.')

        fname = self.current_job.url.replace('http://', '').replace('/', '_')

        if not os.path.exists(self.__dir):
            os.makedirs(self.__dir)

        fpath = self.__dir + '/' + fname + '.json'

        with open(fpath, 'w') as fout:
            json.dump(dlist, fout)

        self.__log(1, '%d records are dumped to \'%s\'' % (len(dlist), fpath))

    def dumpNewJobs(self, root):
        jlist = list()
        if hasattr(self.current_job.module, 'new_jobs'):

            self.__log(3, 'Finding new jobs:')

            for nj in self.current_job.module.new_jobs:
                el = root.xpath(nj['path'])
                for e in el:
                    if nj.has_key('prefix'):
                        job_url = nj['prefix'] + e.attrib['href']
                    else:
                        job_url = e.attrib['href']

                    jlist.append('\t'.join([job_url, nj['module']]) + '\n')

                    self.__log(3, 'Module: %s, Url: %s' % (nj['module'], job_url), indent=1)

            with open(self.jobFile, 'a+') as fout:
                fout.writelines(jlist)

        self.__log(2, '%d new jobs are added.' % len(jlist))

    def extractData(self, root):
        dlist = list()
        elements = root.xpath(self.current_job.module.elements['path'])

        # print len(elements)
        # Quicknote: xpath always return a "list" of elements no matter how many items
        #            are matched

        self.__log(2, '%d elements are found.' % len(elements))
        self.__log(3, 'Extracting attributes of elements:')
        
        for e in elements:
            d = {}
            d['timestamp'] = self.lastRequestTime

            for key, info in self.current_job.module.elements['attributes'].iteritems():

                self.__log(3, '[%s] Info: %s' % (key, str(info)), indent=1)
                
                if info.has_key('path'):
                    ee = e.xpath(info['path'])
                    if len(ee) == 0:
                        d[key] = None
                        continue
                else:
                    ee = [e]

                if info.has_key('function'):
                    f = info['function']
                    v = [f(x) for x in ee]
                elif info.has_key('attrib'):
                    if info['attrib'] == 'text':
                        # v = [x.text for x in ee]
                        v = ee
                    elif info['attrib'] == 'html':
                        v = [etree.tostring(x) for x in ee]
                    else:
                        v = [(x.attrib[info['attrib']] if x.attrib.has_key(info['attrib']) else '') for x in ee]

                if info.has_key('regex') and v is not None:
                    if type(v) == list:
                        v = [re.findall(info['regex'], x)[0] if re.findall(info['regex'], x) else None for x in v]
                    else:
                        v = re.findall(info['regex'], v)[0] if re.findall(info['regex'], v) else None

                # print v
                
                self.__log(3, '[%s] Value: %s' % (key, str(v)), indent=1)
                
                d[key] = v

            dlist.append(d)

        return dlist

    def loadModule(self, module):
        import importlib
        try:
            m = importlib.import_module('module.%s' % module)
        except (ImportError) as e:
            raise ModuleError('No module named %s.' % module)

        return m

