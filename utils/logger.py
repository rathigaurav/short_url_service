import logging
# from logging.handlers import RotatingFileHandler

class LoggerService():
    _self = None
    def __new__(cls):
        # Singleton pattern to ensure only one instance is created
        if not cls._self:
            cls._self = super().__new__(cls)
        return cls._self
    
    def __init__(self, log_file="logs/app.log"):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.logger = logging.getLogger("MyLogger")
            self.logger.setLevel(logging.DEBUG)
            self.setup_logger(log_file)
            

    def setup_logger(self,log_file):
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        # File Handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        # Formatter
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        # Add handlers to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    
    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
