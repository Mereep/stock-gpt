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
# Brief: Interface for MarketIndicator Repository                  		#
#########################################################################
from __future__ import annotations

from abc import abstractmethod

from datatypes.market_indicator import MarketIndicator
from repository.i_repository import IRepository


class IMarketIndicatorRepository(IRepository[MarketIndicator]):

    @abstractmethod
    def get(self, key: str) -> MarketIndicator | None:
        pass

    @abstractmethod
    def store(self, key: str, value: MarketIndicator):
        pass

    @abstractmethod
    def list_keys(self) -> list[str]:
        pass
