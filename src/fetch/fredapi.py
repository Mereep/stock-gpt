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
# Brief: Functions to fetch from the FRED API                     		#
#########################################################################
from __future__ import annotations

import datetime
import logging
from typing import Iterable

import pandas as pd
from fredapi import Fred

from datatypes.market_indicator import MarketIndicator
from misc.config import AppConfig
from repository.market_indicator.i_market_indicator_repository import IMarketIndicatorRepository


def build_fred(app_config: AppConfig) -> Fred:
    """Build a FRED API client from the given configuration"""
    fred = Fred(api_key=app_config.fred_api_key)
    return fred


def get_indicator(
        logger: logging.Logger,
        app_config: AppConfig, indicator_id: str,
        from_date: datetime.date | None = None,
        to_date: datetime.date | None = None) -> MarketIndicator:
    """ Get the indicator with the given ID from the FRED API  """
    fred = build_fred(app_config)
    logger.info(f'Fetching indicator {indicator_id} from FRED API (Code: 324234820)')
    indicator: pd.Series = fred.get_series(indicator_id,
                                           observation_start=from_date,
                                           observation_end=to_date
                                           )

    return MarketIndicator({datetime.date(year=k.year,
                                          month=k.month,
                                          day=k.day): v
                            for k, v in indicator.to_dict().items()})


def load_market_indicators(
        logger: logging.Logger,
        app_config: AppConfig, indicators: list[str],
        from_date: datetime.date | None = None,
        to_date: datetime.date | None = None) -> Iterable[str, dict[datetime.date, float]]:
    """Loads the market indicators for the given time period"""

    for indicator in indicators:
        try:
            indicator_data = get_indicator(app_config=app_config, logger=logger,
                                           indicator_id=indicator,
                                           from_date=from_date,
                                           to_date=to_date)
            yield indicator, indicator_data
        except Exception as e:
            logger.warning(
                f'Could not load indicator {indicator} from FRED API due to {e}. Skipping. (Code: 42834092)')


def update_market_indicators(
        logger: logging.Logger,
        app_config: AppConfig,
        repo: IMarketIndicatorRepository,
        indicators: list[str],
        from_date: datetime.date | None = None,
        to_date: datetime.date | None = None) -> None:
    """ Updates the market indicators for the given time period (files)

    Args:
        logger (logging.Logger): The logger to use
        indicators (list[str]): The indicators to refresh
        app_config (AppConfig): The application configuration
        from_date (datetime.date, optional): The start time. Defaults to `None`.
        to_date (datetime.date, optional): The end time. Defaults to `None`.
        repo (IMarketIndicatorRepository): The repository to use
    """

    indicators = load_market_indicators(app_config=app_config,
                                        logger=logger,
                                        indicators=indicators,
                                        from_date=from_date,
                                        to_date=to_date)

    for indicator, indicator_data in indicators:
        repo.store(key=indicator,
                   value=indicator_data)
