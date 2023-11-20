#########################################################################
# {Stock GPT - Prompt Templates for LLM Stock Analysis}					#
# Copyright (C) 2023 Richard Vogel     									#
#																		#
# This program is free software: you can redistribute it and/or modify	#
# it under the terms of the GNU General Public License as published by	#
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.									#
#																		#
# This program is distributed in the hope that it will be useful,		#
# but WITHOUT ANY WARRANTY; without even the implied warranty of 		#
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 		#
# GNU General Public License for more details. 							#
# #######################################################################
# Brief: Loggers used in the project                              		#
#########################################################################

import logging

_STOCKGPT_LOGGER = None
_CLI_LOGGER = None
_FRED_API_LOGGER = None
_UI_LOGGER = None


def get_default_logger() -> logging.Logger:
    """Get the default logger"""
    global _STOCKGPT_LOGGER
    if _STOCKGPT_LOGGER is None:
        logger = logging.getLogger("stockgpt")
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # add formatter to handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        # add handler to logger
        logger.addHandler(ch)
        _STOCKGPT_LOGGER = logger

    return _STOCKGPT_LOGGER


def get_fred_api_logger() -> logging.Logger:
    """Get the FRED API child logger"""
    global _FRED_API_LOGGER
    if _FRED_API_LOGGER is None:
        logger = get_default_logger()
        fred_api_logger = logger.getChild("fredapi")
        _FRED_API_LOGGER = fred_api_logger

    return _FRED_API_LOGGER


def get_default_cli_logger() -> logging.Logger:
    """Get the default CLI logger"""
    global _CLI_LOGGER
    if _CLI_LOGGER is None:
        logger = get_default_logger()
        _CLI_LOGGER = logger.getChild("cli")

    return _CLI_LOGGER


def get_ui_logger() -> logging.Logger:
    """Get the UI logger"""
    global _UI_LOGGER
    if _UI_LOGGER is None:
        logger = get_default_logger()
        _UI_LOGGER = logger.getChild("ui")

    return _UI_LOGGER