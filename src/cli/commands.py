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
# Brief: CLI command worker functions                                   #
#########################################################################
from __future__ import annotations

import datetime
import logging

from fetch.fredapi import update_market_indicators
from fetch.newsapi import fetch_latest_stock_news
from fetch.stocks import update_stock_symbol, update_all_stock_indicators_for_active_stocks, update_stock_indicators
from generate.gpt import generate_gpt_query
from misc.config import AppConfig
import gettext

from repository.market_indicator.i_market_indicator_repository import IMarketIndicatorRepository
from repository.news.i_news_article_repository import INewsArticleRepository
from repository.stock_indicator.i_stock_indicator_repository import IStockIndicatorRepository
from repository.stock_value.i_stock_value_repository import IStockValueRepository

_ = gettext.gettext


def update_market_indicator_data(
        app_config: AppConfig,
        repo: IMarketIndicatorRepository,
        logger: logging.Logger,
        indicators: list[str],
        from_date: datetime.date | None = None,
        to_date: datetime.date | None = None,
) -> None:
    """Refreshes the indicator data for the given time period

    Args:
        logger (logging.Logger): The logger to use
        indicators (list[str]): The indicators to refresh
        from_date (datetime.date, optional): The start time. Defaults to `None`.
        to_date (datetime.date, optional): The end time. Defaults to `None`.
        app_config (AppConfig): The application configuration
        repo (IMarketIndicatorRepository): The repository to use
    """
    logger.info(_("Collecting indicators for: {indicators} (from: {d_from} to {d_to})").format(
        indicators=indicators,
        d_from=from_date,
        d_to=to_date,
    ))

    update_market_indicators(app_config=app_config,
                             logger=logger,
                             repo=repo,
                             indicators=indicators,
                             from_date=from_date,
                             to_date=to_date)


def update_stock_symbol_data(
        repo: IStockValueRepository,
        logger: logging.Logger,
        symbol: str,
        from_date: datetime.date | None = None,
        to_date: datetime.date | None = None,
) -> None:
    """Refreshes the stock data for the given time period

    Args:
        logger (logging.Logger): The logger to use
        symbol (str): The stock symbol to refresh
        from_date (datetime.date, optional): The start time. Defaults to `None`.
        to_date (datetime.date, optional): The end time. Defaults to `None`.
        repo (IStockValueRepository): The repository to use
    """
    logger.info(_("Collecting data for: {symbol} (from: {d_from} to {d_to})").format(
        symbol=symbol,
        d_from=from_date,
        d_to=to_date,
    ))

    update_stock_symbol(repo=repo,
                        logger=logger,
                        symbol=symbol,
                        from_date=from_date,
                        to_date=to_date)


def update_stock_indicator_data(
        stock_value_repo: IStockValueRepository,
        stock_indicator_repo: IStockIndicatorRepository,
        indicators_to_update: list[str],
        logger: logging.Logger):
    logger.info(_("Updating stock data for all active stocks"))
    update_all_stock_indicators_for_active_stocks(
        stock_value_repo=stock_value_repo,
        stock_indicator_repo=stock_indicator_repo,
        indicators_to_update=indicators_to_update,
        logger=logger)


def update_news_data(
        symbol: str,
        logger: logging.Logger,
        repo: INewsArticleRepository,
        news_api_key: str,
        page_size: int = 15):
    """ Refreshes the news data for the given stock symbol
    Args:
        symbol (str): The stock symbol to refresh
        logger (logging.Logger): The logger to use
        repo (INewsArticleRepository): The repository to use
        news_api_key (str): The news api key to use
        page_size (int, optional): The number of articles to fetch. Defaults to 15.
    """
    logger.info(_("Collecting news for: {symbol}").format(symbol=symbol))
    news = fetch_latest_stock_news(stock_symbol=symbol,
                                   page_size=page_size,
                                   api_key=news_api_key)

    repo.store(key=symbol, value=news)


def generate_query(
        logger: logging.Logger,
        symbol: str,
        day: datetime.date,
        stock_value_repo: IStockValueRepository,
        stock_indicator_repo: IStockIndicatorRepository,
        market_indicator_repo: IMarketIndicatorRepository,
        market_indicators_max_value_count: int,
        stock_indicators_max_age: int,
        stock_values_max_age: int,
        max_news_age: int,
        news_repo: INewsArticleRepository | None = None,
        update_stock_symbol: bool = False,
        stock_indicators_to_update: list[str] | None = None,
        news_api_key: str | None = None,
):
    """ Generates a query for the given stock symbol

    Args:
        logger (logging.Logger): The logger to use
        symbol (str): The stock symbol to query
        day (datetime.date): The day to query
        news_repo (INewsArticleRepository): The news repository to use
        stock_value_repo (IStockValueRepository): The stock value repository to use
        stock_indicator_repo (IStockIndicatorRepository): The stock indicator repository to use
        market_indicator_repo (IMarketIndicatorRepository): The market indicator repository to use
        market_indicators_max_value_count (int): The maximum number of market indicator values to query
        stock_indicators_max_age (int): The maximum age of stock indicators to query
        stock_values_max_age (int): The maximum age of stock values to query
        max_news_age (int): The maximum age of news articles to query
        update_stock_symbol (bool, optional): Whether to update the stock symbol. Defaults to False.
        news_repo (INewsArticleRepository | None, optional): The news repository to use. Defaults to None.
        news_api_key (str, optional): The news api key to use. Defaults to None.
        only needed when updating the stock symbol
        stock_indicators_to_update (list[str] | None, optional): The stock indicators to update.
        Only needed when updating the stock symbol.
    """
    if update_stock_symbol:
        logger.info(_("Updating stock symbol data for: {symbol} (Code: 29408230)").format(symbol=symbol))
        update_stock_symbol_data(
            repo=stock_value_repo,
            logger=logger,
            symbol=symbol,
        )

        update_news_data(symbol=symbol,
                         repo=news_repo,
                         news_api_key=news_api_key,
                         logger=logger, )

        stock_info = stock_value_repo.get(key=symbol)
        update_stock_indicators(
            stock_info=stock_info,
            repo=stock_indicator_repo,
            indicators_to_update=[],
            logger=logger,
        )

    res = generate_gpt_query(
        logger=logger,
        symbol=symbol,
        for_date=day,
        stock_value_repo=stock_value_repo,
        stock_indicator_repo=stock_indicator_repo,
        market_indicator_repo=market_indicator_repo,
        news_repo=news_repo,
        market_indicators_max_value_count=market_indicators_max_value_count,
        stock_indicators_max_age=stock_indicators_max_age,
        stock_values_max_age=stock_values_max_age,
        max_news_age=max_news_age,
    )

    print(res)
