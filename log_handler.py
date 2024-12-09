import logging

class LogHandler():

    def __init__(self, datetime):

        # initalize logging and set level
        self.logger = logging.getLogger('RVA Calls Logger')
        self.logger.setLevel(logging.DEBUG)
        
        # create file handler and set level to debug
        file = f'run_{datetime}.log'
        file_handler = logging.FileHandler(filename=file, mode="a")
        file_handler.setLevel(logging.DEBUG)

        # logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to file_handler
        file_handler.setFormatter(formatter)

        # add file_handler to logger
        self.logger.addHandler(file_handler)

    def debug_message(self, message):
        return self.logger.debug(message)
    
    def info_message(self, message):
        return self.logger.info(message)
    
    def warning_message(self, message):
        return self.logger.warning(message)
    
    def error_message(self, message):
        return self.logger.error(message)

