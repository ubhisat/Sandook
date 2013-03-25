import logging


class SULog(object):
    def __init__(self, config=None):

        self._logger = logging.getLogger('gtasks-cl')
        self._hdlr = logging.FileHandler(config.log_path) if config else \
            logging.FileHandler('./config')
        self._formatter = logging.Formatter('%(asctime)s %(levelname)s %('
                                        'message)s')
        self._hdlr.setFormatter(self._formatter)
        self._logger.addHandler(self._hdlr)
        self._logger.setLevel(logging.INFO)

        self.logw = self._logger.warn
        self.logi = self._logger.info
        self.loge = self._logger.error
