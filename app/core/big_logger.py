import logging
import asyncio
import sys
from pathlib import Path
from typing import Callable
from logging.handlers import RotatingFileHandler
from .config import get_logger_config


class BigLogger:

    def __init__(
            self,
            logger_name: str = __name__
    ):
        settings = get_logger_config()
        self.name: str = logger_name
        self.log_instance = logging.getLogger(self.name)
        self.log_instance.setLevel(settings.LEVEL)
        self.log_instance.propagate = False

        if not self.log_instance.handlers:
            _format: logging.Formatter = logging.Formatter(
                "[%(asctime)s] | [%(levelname)s] | [%(name)s] | [%(message)s]"
            )
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(_format)
            self.log_instance.addHandler(console_handler)

            _fh = self.__get_filehandler(settings.FILE_NAME)
            _fh.setFormatter(_format)
            self.log_instance.addHandler(_fh)


    def __get_filehandler(self, log_file:str ):
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        file_path = log_dir / log_file

        return RotatingFileHandler(
            file_path,
            maxBytes=5 * 1024 * 1024,
            backupCount=5
        )

    def info(self, message: str):
        self.log_instance.info(message)

    def debug(self, message: str):
        self.log_instance.debug(message)

    def error(self, message: str):
        self.log_instance.error(message)

    def warning(self, message: str):
        self.log_instance.warning(message)


    def error_decorator(self, reraise: bool = True):

        def decorator(fn: Callable):
            if asyncio.iscoroutinefunction(fn):
                # IF Fn is async

                async def async_wrapper(*args, **kwargs):
                    try:
                        return await fn(*args, **kwargs)

                    except Exception as e:
                        self.log_instance.error(
                            f"Exception in {fn.__name__} : {str(e)}",
                            exc_info=True
                        )

                        if reraise:
                            raise

            else:
                def sync_wrapper(*args, **kwargs):
                    try:
                        return fn(*args, **kwargs)
                    except Exception as e:
                        self.log_instance.error(
                            f"Exception in {fn.__name__} : {str(e)}",
                            exc_info=True
                        )

                        if reraise:
                            raise
