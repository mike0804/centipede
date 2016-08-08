# -*- coding: utf-8 -*-

from .exceptions import Error, JobError, ModuleError
import models 

def Centipede(fname, selenium, **kwargs):    
    if selenium:
        return models.Centipede_Selenium(fname, **kwargs)
    else:
        return models.Centipede(fname, **kwargs)