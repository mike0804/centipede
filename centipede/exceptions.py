# -*- coding: utf-8 -*-

class Error(Exception):
    pass

class JobError(Error):

    FILE_NOT_FOUND = 0

    INVALID_FORMAT = 1
    INVALID_NAME = 4
    INVALID_URL = 2
    INVALID_MODULE_NAME = 3

    __messages = [
        'File not found: %s',

        'Invalid job format: %s',
        'Invalid job url: %s',
        'Invalid job module name: %s',
        'Invalid job name: %s',
    ]

    def __init__(self, errno, vars):
        self.msg = self.__messages[errno] % vars

class ModuleError(Error):

    MODULE_NOT_FOUND = 0
    
    __messages = [
        'Module not found: %s',
    ]

    def __init__(self, errno, vars):
        self.msg = self.__messages[errno] % vars