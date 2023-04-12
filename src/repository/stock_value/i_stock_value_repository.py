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
# Brief: Interface for StockValue (Chart) Repository                    #
#########################################################################
from abc import abstractmethod

from datatypes.stock_data import StockDataInfo
from repository.i_repository import IRepository


class IStockValueRepository(IRepository[StockDataInfo]):

    @abstractmethod
    def get(self, key: str) -> StockDataInfo:
        pass

    @abstractmethod
    def store(self, key: str, value: StockDataInfo):
        pass

    @abstractmethod
    def list_keys(self) -> list[str]:
        pass
