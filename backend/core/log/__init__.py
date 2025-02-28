import os
import sys
import logging
import logging.handlers


class Log:
    def __init__(self, log_path='log/', log_name='server.log', log_level=logging.DEBUG):
        if not os.path.exists(log_path):
            os.mkdir(log_path)

        log_file = log_path + log_name
        fmt = '%(levelname)s %(asctime)s [process: %(process)d:][thread: %(thread)d] %(pathname)s [line:%(lineno)d] %(message)s'
        handler = logging.handlers.TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=3)

        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(fmt)
        console_handler.setFormatter(console_formatter)

        self.LOGGER = logging.getLogger(__name__)
        self.LOGGER.setLevel(log_level)
        self.LOGGER.addHandler(handler)
        self.LOGGER.addHandler(console_handler)

    def get_log(self):
        return self.LOGGER


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

log_name = 'temp.log'
if 'llm_tasks' in sys.argv[0]:
    log_name = 'llm_tasks.log'

logger = Log(log_path=BASE_DIR + '/log/', log_level=logging.DEBUG, log_name=log_name).get_log()
