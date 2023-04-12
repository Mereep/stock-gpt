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
# Brief: Interface for the News Article Repository                  	#
#########################################################################
from __future__ import annotations

from abc import abstractmethod

from datatypes.news_article import NewsArticle, TNewsArticles
from repository.i_repository import IRepository


class INewsArticleRepository(IRepository[TNewsArticles]):

    @abstractmethod
    def get(self, key: str) -> TNewsArticles | None:
        pass

    @abstractmethod
    def store(self, key: str, value: TNewsArticles):
        pass

    @abstractmethod
    def list_keys(self) -> list[str]:
        pass
