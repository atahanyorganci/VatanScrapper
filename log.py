from datetime import datetime, timedelta
import traceback
import sys

INFO = 0
DEBUG = 1
WARNING = 2
ERROR = 3
CRITICAL = 4


class Logger:
    def __init__(self, level: int, timed=True, time_str='%H:%M:%S'):
        self.__level = level
        self.__timed = timed
        self.__time_str = time_str

    def setLevel(self, level):
        self.__level = level

    def getLevel(self):
        return self.__level

    def timeEvent(self, func):
        start = timedelta()
        func()
        end = timedelta()
        delta = timedelta.total_seconds(end - start)
        self.info(f'{func} took {delta} seconds.')

    def verbose(self, message):
        dt = datetime.now().strftime('%d %B %Y %H:%M:%S')
        print(f'VERBOSE: {dt}: {message}')

    def info(self, message: str):
        if INFO >= self.__level:
            if self.__timed:
                print(f'INFO: {self._getTime()}: {message}')
            else:
                print(f'INFO: {message}')

    def debug(self, message: str):
        if DEBUG >= self.__level:
            if self.__timed:
                print(f'DEBUG: {self._getTime()}: {message}')
            else:
                print(f'DEBUG: {message}')

    def warning(self, message: str):
        if WARNING >= self.__level:
            if self.__timed:
                print(f'WARNING: {self._getTime()}: {message}')
            else:
                print(f'WARNING: {message}')

    def error(self, message: str):
        if ERROR >= self.__level:
            if self.__timed:
                print(f'ERROR: {self._getTime()}: {message}')
            else:
                print(f'ERROR: {message}')

    def critical(self, message: str):
        if INFO >= self.__level:
            if self.__timed:
                print(f'CRITICAL: {self._getTime()}: {message}')
            else:
                print(f'CRITICAL: {message}')

    def _getTime(self):
        return datetime.now().strftime(self.__time_str)

    def trace(self, ex):
        traceback.print_exception(type(ex), ex, None)
