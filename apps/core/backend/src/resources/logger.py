import logging


class Logger():
    @staticmethod
    def info(self, message: str):
        logging.info(message)

    @staticmethod
    def warning(self, message: str):
        logging.warning(message)

    @staticmethod
    def error(self, message: str):
        logging.error(message)


