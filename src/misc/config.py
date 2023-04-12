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
# Brief: Config object holding general moving parts                     #
# All the keys can be configured via environment variables using template:
# `STOCKGPT_<KEY_NAME_IN_UPPERCASE>`                                    #
#########################################################################
# Description:

from __future__ import annotations

import dataclasses
import os
from pathlib import Path

from exceptions.config import StockGptConfigException
from misc.utils import read_market_indicator_defaults, read_stock_indicator_defaults


@dataclasses.dataclass
class AppConfig:
    """
    Configuration class for the application. Loads settings from environment variables.
    """
    fred_api_key: str | None = dataclasses.field(default=None)
    news_api_key: str | None = dataclasses.field(default=None)

    data_base_dir: str = dataclasses.field(
        default=(Path(__file__).parent.parent.parent / 'data').absolute())

    default_market_indicators: list[str] = dataclasses.field(default_factory=lambda: [])
    default_stock_indicators: list[str] = dataclasses.field(default_factory=lambda: [])

    @property
    def market_indicator_base_dir(self) -> Path:
        return self.data_base_dir / 'stock_data' / 'market_indicators'

    @property
    def default_market_indicator_dictionary_file(self) -> Path:
        return self.data_base_dir / 'defaults' / 'market_indicators.csv'

    @property
    def default_stock_indicator_dictionary_file(self) -> Path:
        return self.data_base_dir / 'defaults' / 'stock_indicators.csv'

    @property
    def stock_value_base_dir(self) -> Path:
        return self.data_base_dir / 'stock_data' / 'stock_values'

    @property
    def default_news_article_base_dir(self) -> Path:
        return self.data_base_dir / 'stock_data' / 'news_articles'

    @property
    def stock_indicators_base_dir(self) -> Path:
        return self.data_base_dir / 'stock_data' / 'stock_indicators'

    @classmethod
    def from_env(cls) -> 'Self':
        collected_env = {}
        for key in [key for key in cls.__dict__.keys() if not key.startswith('_')]:
            env_name = f'STOCKGPT_{key.upper()}'
            if env_name in os.environ:
                collected_env[key] = os.environ[env_name]
        return cls(**collected_env)

    def __post_init__(self):
        required_paths = {
            'data_base_dir': self.data_base_dir,
            'market_indicator_base_dir': self.market_indicator_base_dir,
            'stock_value_base_dir': self.stock_value_base_dir,
            'default_market_indicator_dictionary_file': self.default_market_indicator_dictionary_file,
            'default_stock_indicator_dictionary_file': self.default_stock_indicator_dictionary_file,
            'stock_indicators_base_dir': self.stock_indicators_base_dir,
            'default_news_article_base_dir': self.default_news_article_base_dir,
        }

        for name, path in required_paths.items():
            if not path.exists():
                raise StockGptConfigException(f"{name.capitalize().replace('_', ' ')} {path} does not exist (Code: 324234234)")

        if isinstance(self.default_market_indicators, str):
            self.default_market_indicators = [i.strip() for i in self.default_market_indicators.split(',')]
        else:
            defaults = read_market_indicator_defaults(self.default_market_indicator_dictionary_file)
            self.default_market_indicators = list(defaults.keys())

        if len(self.default_market_indicators) == 0:
            raise StockGptConfigException("No default market indicators given (Code: 39812093812)")

        if isinstance(self.default_stock_indicators, str):
            self.default_stock_indicators = [i.strip() for i in self.default_stock_indicators.split(',')]
        else:
            defaults = read_stock_indicator_defaults(self.default_stock_indicator_dictionary_file)
            self.default_stock_indicators = list(defaults.keys())

        if self.fred_api_key is None or not self.fred_api_key:
            raise StockGptConfigException("No FRED API key given (use environment the variable"
                                          " STOCKGPT_FRED_API_KEY) (Code: 3940ß29340)")

        if self.news_api_key is None or not self.news_api_key:
            raise StockGptConfigException("No News API key given (use environment the variable"
                                          " STOCKGPT_NEWS_API_KEY) (Code: 3249823094)")