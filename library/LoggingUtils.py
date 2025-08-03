from wpilib import SmartDashboard
from wpiutil._wpiutil import Sendable

import functools

'''
ref: https://github.com/SciBorgs/Hydrogen/blob/reefscape/src/main/java/org/sciborgs1155/lib/LoggingUtils.java

THIS IS VERY DIFFERENT FROM THE JAVA VERSION! WE USE SMARTDASHBOARD HERE
BUT THE JAVA VERSION USES EPILOGUE! THIS IS MEANT TO BE SIMILAR-ISH!
'''


def logNumber(key:str, value:int):
    SmartDashboard.putNumber(key, value)

def logBoolean(key:str, value:bool):
    SmartDashboard.putBoolean(key, value)

def logString(key:str, value:str):
    SmartDashboard.putString(key, value)

def logValue(key:str, value):
    SmartDashboard.putValue(key, value)

def logRaw(key:str, value):
    SmartDashboard.putRaw(key, value)

def log(key:str, value:Sendable):
    SmartDashboard.putData(key, value)

def Log(func):
    '''
    EXPERIMENTAL logging decorator based on class and function name. Not very pretty.
    '''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        log("/Robot/{}/{}".format(func.__class__, func.__name__), value)
    return wrapper