# coding: utf-8
import hues
import os
import platform
import re
from collections import namedtuple
import properties
from logging import Formatter

# Unicorns
from hues.huestr import HueString as huestr
from hues.console import Config, SimpleConsole, PowerlineConsole

p_sys_type = platform.system()
as_tuples = lambda name, obj: namedtuple(name, obj.keys())(**obj)

DEBUG = 0
WARNING = 1
INFO = 2
SUCCESS = 3
ERROR = 4

logging_config = properties.logger_config \
    if hasattr(properties, 'logger_config') and properties.logger_config \
    else \
    {
        # 'filename': 'app.log',
        # 'level': 'logging.DEBUG',
        'format': '%(levelname)s : (%(asctime)s) ==> ::: %(message)s',
        # 'format': '%(levelname)s %(name)s: <%(module)s> (%(asctime)s) ==> %(filename)s {%(funcName)s} [line:%(lineno)d] ::: %(message)s',
        'time_format': '%Y-%m-%d %H:%M:%S',
        'show_time': 'yes',
        'add_newline': 'yes',
        'theme': 'simple'
    }

# 默认等级为INFO
LOG_LEVEL = eval(logging_config['level'].upper()) if 'level' in logging_config else INFO

conf = Config()

setattr(conf, 'opts', as_tuples('Options', logging_config))

console = SimpleConsole(conf=conf)


# 日志过滤非框架打印
class DefFilter:
    """
    默认过滤器
    """

    def filter(self, record):
        return eval(record['level'].upper()) >= LOG_LEVEL and record.name.startswith('dophon') and record.levelno >= \
               logging_config['level']


def level_filter(f):
    def args(*args,**kwargs):
        if 'level' in kwargs:
            # print('level_filter:',kwargs['level'])
            _level = kwargs['level']
        else:
            # print('level_filter:',args[1])
            _level = args[1]
        return f(*args,**kwargs) if _level >= LOG_LEVEL else None
    return args


class DefFormatter:
    """
    默认格式管理器
    """

    def __init__(self, fmt_rule: str = logging_config):
        self._fmt_rule = fmt_rule

    def format(self, message: object):
        return self._fmt_rule % message if isinstance(message, tuple) else str(message)


class DophonLogger:
    _filter = DefFilter()
    _formatter = DefFormatter()

    def __init__(self, *args, **kwargs):
        self.logger = console
        # hues.SimpleConsole.conf = conf
        # for name in dir(conf.opts):
        #     print(f'{name} ==> {getattr(conf.opts,name)}')

    def __getattr__(self, item):
        if callable(item):
            print('callable !')
        else:
            pass

    def debug(self, message: object, *args, **kwargs):
        if args:
            message = f'{message % args}'
        self._debug(DEBUG, self._formatter.format(message))

    def warning(self, message: object, *args, **kwargs):
        if args:
            message = f'{message % args}'
        self._warning(WARNING, self._formatter.format(message))

    def warn(self, message: object, *args, **kwargs):
        if args:
            message = f'{message % args}'
        self._warning(WARNING, self._formatter.format(message))

    def info(self, message: object, *args, **kwargs):
        if args:
            message = f'{message % args}'
        self._info(INFO, self._formatter.format(message))

    def success(self, message: object, *args, **kwargs):
        if args:
            message = f'{message % args}'
        self._success(INFO, self._formatter.format(message))

    def error(self, message: object, *args, **kwargs):
        if args:
            message = f'{message % args}'
        self._error(ERROR, self._formatter.format(message))

    def log(self, message: object, *args, **kwargs):
        if args:
            message = f'{message % args}'
        self.logger.log(self._formatter.format(message))

    @level_filter
    def _debug(self, level: int, message: object):
        self.logger.log(huestr('DEBUG').blue.colorized, '-', str(message))

    @level_filter
    def _warning(self, level: int, message: object):
        self.logger.warn(str(message))

    @level_filter
    def _info(self, level: int, message: object):
        self.logger.info(str(message))

    @level_filter
    def _success(self, level: int, message: object):
        self.logger.success(str(message))

    @level_filter
    def _error(self, level: int, message: object):
        self.logger.error(str(message))

    def addFilter(self, filter):
        self._filter = filter


def inject_logger(g: dict, var_name: str = 'logger'):
    # logger = logging.getLogger('dophon.' + re.sub('\..*', '', g['__file__'].split(os.path.sep)[-1]))
    logger = DophonLogger('dophon.' + re.sub('\..*', '', g['__file__'].split(os.path.sep)[-1]))
    # logger.addFilter(DefFilter())
    g[var_name] = logger
