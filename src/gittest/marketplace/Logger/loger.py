from __future__ import annotations

import logging

from dynaconf import Dynaconf


class Logger:
    def __init__(self, config_name: str) -> None:
        self.settings = Dynaconf(settings_files=[config_name])
        self.py_logger = logging.getLogger(__name__)
        self.py_logger.setLevel(eval(self.settings.logger_settings.level))
        py_handler = logging.FileHandler(self.settings.logger_settings.filename,
                                         mode=self.settings.logger_settings.filemode)
        py_formatter = logging.Formatter(self.settings.logger_settings.format, datefmt='%d.%m.%Y %H:%M:%S')
        py_handler.setFormatter(py_formatter)
        self.py_logger.addHandler(py_handler)

    def get_logger(self) -> logging.Logger:
        return self.py_logger


logger = Logger("pyproject.toml").get_logger()
