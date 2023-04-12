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
# Brief: Functions to fetch Stock Infos (as in from yfinance)     		#
#########################################################################
from __future__ import annotations

import datetime
import logging

import requests
import yfinance

from datatypes.stock_data import StockDataInfo, StockDataChartEntry
from datatypes.stock_indicator import StockIndicators
from exceptions.base import StockGptException
from misc.stock_indicator_util import get_stock_indicator_by_id
from repository.stock_indicator.i_stock_indicator_repository import IStockIndicatorRepository
from repository.stock_value.i_stock_value_repository import IStockValueRepository

YF_FINANCE_BASE_URL = 'https://query2.finance.yahoo.com/v8/finance/chart/{}'
YF_FINANCE_UA_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'
}


def load_stock_symbol_from_yfinance(
        symbol: str,
        logger: logging.Logger,
        from_date: datetime.date | None = None,
        to_date: datetime.date | None = None) -> StockDataInfo:
    """Loads the stock data for the given symbol.

    Args:
        symbol (str): The symbol to load.
        logger (logging.Logger): The logger to use.
        from_date (datetime.date, optional): The start date. Defaults to None.
        to_date (datetime.date, optional): The end date. Defaults to None.

    Returns:
        StockDataInfo: The stock data result object.
    """
    base_url = YF_FINANCE_BASE_URL.format(symbol)
    from_date = from_date or datetime.date.today() - datetime.timedelta(days=365)
    to_date = to_date or datetime.date.today()

    # datetime.date -> timestamp
    from_date = int(datetime.datetime(from_date.year, from_date.month, from_date.day).timestamp())

    to_date = int(datetime.datetime(to_date.year, to_date.month, to_date.day).timestamp())
    to_date += + 24*60*60-1  # last second of the day
    logger.info(f'Loading stock data for symbol {symbol} (Code: 39483092)')
    request = requests.get(base_url,
                           params={'period1': from_date,
                                   'period2': to_date,
                                   'interval': '1d'},
                           headers=YF_FINANCE_UA_HEADER)

    data = request.json()
    if data['chart']['error']:
        raise StockGptException(f"Error loading stock data for symbol {symbol}: {data['chart']['error']} (Code: 4289342)")

    indicators = data['chart']['result'][0]['indicators']['quote'][0]
    highs, lows, opens, closes, volumes = (
        indicators[key] for key in ('high', 'low', 'open', 'close', 'volume')
    )
    timestamps = data['chart']['result'][0]['timestamp']

    entries = {
        datetime.date.fromtimestamp(timestamp): StockDataChartEntry(high=high, low=low, open=open,
                                                                    close=close, volume=volume)
        for high, low, open, close, volume, timestamp in zip(highs, lows, opens, closes, volumes, timestamps)
    }

    return StockDataInfo(symbol=symbol, chart=entries)


def update_stock_symbol(repo: IStockValueRepository,
                        symbol: str,
                        logger: logging.Logger,
                        from_date: datetime.date | None = None,
                        to_date: datetime.date | None = None) -> None:
    """Updates the stock values (charts).

    Args:
        repo (IStockValueRepository): The repository to use.
        symbol (str): The symbol to update.
        logger (logging.Logger): The logger to use.
        from_date (datetime.date, optional): The start date. Defaults to None.
        to_date (datetime.date, optional): The end date. Defaults to None.
    """
    data = load_stock_symbol_from_yfinance(symbol=symbol,
                                           logger=logger,
                                           from_date=from_date,
                                           to_date=to_date)

    repo.store(key=symbol,
               value=data)


def update_all_stock_indicators_for_active_stocks(logger: logging.Logger,
                                                  stock_value_repo: IStockValueRepository,
                                                  stock_indicator_repo: IStockIndicatorRepository,
                                                  indicators_to_update: list[str]
                                                  ) -> None:
    """Updates all active stock indicators.

    Args:
        logger (logging.Logger): The logger to use.
        stock_value_repo (IStockValueRepository): The stock value repository to use.
        stock_indicator_repo (IStockIndicatorRepository): The stock indicator repository to use.
        indicators_to_update (list[str]): The indicators which should be calculated for each stock
    """
    for symbol in stock_value_repo.list_keys():
        logger.info(f'Updating stock symbol {symbol} (Code: 943289023)')
        # update_stock_symbol(symbol=symbol,
        #                     logger=logger)
        stock_info = stock_value_repo.get(symbol)
        update_stock_indicators(stock_info=stock_info,
                                indicators_to_update=indicators_to_update,
                                repo=stock_indicator_repo,
                                logger=logger)


def update_stock_indicators(
        stock_info: StockDataInfo,
        indicators_to_update: list[str],
        logger: logging.Logger,
        repo: IStockIndicatorRepository,
):
    """Updates the stock indicator on the disk repository.

    Args:
        stock_info (StockDataInfo): The stock data info (chart).
        indicators_to_update (list[str]): The indicators to update.
        logger (logging.Logger): The logger to use.
        repo (IStockIndicatorRepository): The repository to use.
    """

    d = {}
    for date in stock_info.chart.keys():
        d[date] = {}
        for indicator_id in indicators_to_update:
            indicator_cls = get_stock_indicator_by_id(indicator_id)

            if not indicator_cls:
                logger.warning(f"Could not find indicator with id {indicator_id}. "
                               f"Skipping (Code: 23489230)")
                continue

            # add a new column if the indicator does not exist
            indicator = indicator_cls()
            value = indicator.calculate(data=stock_info,
                                        for_date=date)
            d[date][indicator_id] = value

    repo.store(key=stock_info.symbol,
               value=StockIndicators(d))
