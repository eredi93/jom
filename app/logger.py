

import time
import logging
from .database import DATABASE, Model, PrimaryKeyField, DateTimeField, \
                         CharField, TextField

# Peewee Logger Model
class Logger(Model):
    """Syslog model"""
    id = PrimaryKeyField()
    created = DateTimeField(null=False)
    name = CharField(max_length=45)
    log_level = CharField(max_length=15)
    message = TextField()
    module = CharField()
    function_name = CharField()
    line_number = CharField()

    class Meta:
        database = DATABASE

# Logging Handler Peewee
class PeeweeHandler(logging.Handler):
    """ Peewee logging handler """
    def __init__(self, Logger):
        """
        :param Logger: Peewee Model object
        :return: mySQLHandler
        """
        logging.Handler.__init__(self)
        self.logger = Logger
        self.create_table()

    def create_table(self):
        """ Create MySQL tables

        :return: void
        """
        from peewee import InternalError
        try:
            self.logger.create_table()
        except InternalError:
            pass

    def format_time(self, created):
        """ Set time with correct format

        :param created: string
        :return: string
        """
        return time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime(created)
        )

    def emit(self, record):
        """ Insert into DB

        :param record: object
        :return: void
        """
        self.format(record)
        self.logger.create(
            created=self.format_time(record.created),
            name=record.name,
            log_level=record.levelname,
            message=record.msg,
            module=record.module,
            function_name=record.funcName,
            line_number=record.lineno
        )

# Set Name and level to logger
def set_logger(logger_name, level='INFO'):
    """ Set logger

    :param logger_name: string
    :param level: string
    :return: void
    """
    handler = PeeweeHandler(Logger)
    logger = logging.getLogger(logger_name)
    logger.addHandler(handler)
    if level.upper() == 'CRITICAL':
        logger.setLevel(logging.CRITICAL)
    elif level.upper() == 'ERROR':
        logger.setLevel(logging.ERROR)
    elif level.upper() == 'WARNING':
        logger.setLevel(logging.WARNING)
    elif level.upper() == 'INFO':
        logger.setLevel(logging.INFO)
    elif level.upper() == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    else:
        pass

# Get logger from name and set level
def get_logger(logger_name, level='INFO'):
    """ Get logger

    :param logger_name: string
    :param level: string
    :return: object
    """
    handler = PeeweeHandler(Logger)
    logger = logging.getLogger(logger_name)
    logger.addHandler(handler)
    if level.upper() == 'CRITICAL':
        logger.setLevel(logging.CRITICAL)
    elif level.upper() == 'ERROR':
        logger.setLevel(logging.ERROR)
    elif level.upper() == 'WARNING':
        logger.setLevel(logging.WARNING)
    elif level.upper() == 'INFO':
        logger.setLevel(logging.INFO)
    elif level.upper() == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    else:
        pass
    return logger

# Setup the database table using Peewee
def init_logger_models():
    """models init function"""
    DATABASE.connect()
    DATABASE.create_tables([Logger], safe=True)
    DATABASE.close()
