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
# Brief: General Interface for all repositories                         #
#########################################################################
from __future__ import annotations

import abc
import logging
from typing import Iterable, TypeVar, Generic


TRepositoryType = TypeVar('TRepositoryType')


class IRepository(abc.ABC, Generic[TRepositoryType]):
    _logger: logging.Logger

    @abc.abstractmethod
    def list_keys(self) -> Iterable[str]:
        pass

    def get(self, key: str) -> TRepositoryType | None:
        """ get by id if available """
        pass

    def store(self, key: str, value: TRepositoryType) -> None:
        """ update or create """
        pass

    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def log_info(self, msg: str):
        self._logger.info(msg)

    def log_debug(self, msg: str):
        self._logger.debug(msg)

    def log_error(self, msg: str):
        self._logger.error(msg)

    def log_warning(self, msg: str):
        self._logger.warning(msg)
