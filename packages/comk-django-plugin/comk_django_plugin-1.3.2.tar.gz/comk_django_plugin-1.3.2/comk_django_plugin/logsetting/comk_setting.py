'''
django 日志教程：

https://segmentfault.com/a/1190000016068105

https://docs.djangoproject.com/en/2.2/topics/logging/

'''
import datetime

from django.conf import settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'comk_verbose': {
            # 'format': '%(levelname)s %(asctime)s %(module)s %(pathname)s %(lineno)d %(process)d %(thread)d %(message)s'
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'comk_request_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': settings.BASE_DIR + '/log/comk_request.log',
            'when': 'MIDNIGHT',
            'interval': 1,
            'backupCount': 7,
            'atTime': datetime.time(0, 0, 0, 0),
            'formatter': 'comk_verbose',
            'encoding': 'utf-8',
        },
        'comk_exception_log': {
            'level': 'DEBUG',  # 打印DEBUG （或更高）级别的消息。
            'class': 'logging.handlers.TimedRotatingFileHandler',  # 它的主体程序是TimedRotatingFileHandler类，按日期切割，这是最重要的。
            'filename': settings.BASE_DIR + '/log/comk_error_traceback.log',
            'when': 'MIDNIGHT',  # 对log文件进行切割的时间，当 when 和 atTime 同时设置时，以 atTime 为准。
            'interval': 1,  # 默认为1
            # 'filename': "./log/comk_error_traceback.log",
            # 'maxBytes': 1024 * 1024 * 100,  # 每个日志文件大小，当文件快到达到 maxBytes 时，会新开一个log文件。
            'backupCount': 7,  # 保留日志的个数，当maxBytes不为0时生效，当新开文件到达 backupCount 个时，会重新覆盖这几个文件。
            'atTime': datetime.time(0, 0, 0, 0),  # 对log文件进行切割的时间，当 when 和 atTime 同时设置时，以 atTime 为准。
            'formatter': 'comk_verbose',  # 采用verbose为格式化器。
            'encoding': 'utf-8',  # 设定编码，如不设定，则编码为ascii，无法写入中文
        },
    },
    'loggers': {
        'comk_request_log': {
            'handlers': ['comk_request_log'],
            'level': 'INFO',
            'propagate': True,
        },
        'comk_exception_log': {
            'handlers': ['comk_exception_log'],
            'level': 'ERROR',
        },
    }
}
