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
# Brief: Interface for StockIndicator Repository (Technical Indicators) #
#########################################################################
from __future__ import annotations

from abc import abstractmethod

from datatypes.stock_indicator import StockIndicators
from repository.i_repository import IRepository


class IStockIndicatorRepository(IRepository[StockIndicators]):

    @abstractmethod
    def get(self, key: str) -> StockIndicators | None:
        pass

    @abstractmethod
    def store(self, key: str, value: StockIndicators):
        pass

    @abstractmethod
    def list_keys(self) -> list[str]:
        pass
