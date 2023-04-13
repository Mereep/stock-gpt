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
# Brief: Functions to generate Prompots                           		#
#########################################################################
from __future__ import annotations

import datetime
import gettext
import logging
from dataclasses import asdict
from random import shuffle

import pandas as pd

from exceptions.base import StockGptException
from fetch.yfinance import fetch_basic_stock_info
from repository.market_indicator.i_market_indicator_repository import IMarketIndicatorRepository
from repository.news.i_news_article_repository import INewsArticleRepository
from repository.stock_indicator.i_stock_indicator_repository import IStockIndicatorRepository
from repository.stock_value.i_stock_value_repository import IStockValueRepository

_ = gettext.gettext


def generate_gpt_query(symbol: str,
                       logger: logging.Logger,
                       stock_value_repo: IStockValueRepository,
                       stock_indicator_repo: IStockIndicatorRepository,
                       market_indicator_repo: IMarketIndicatorRepository,
                       news_repo: INewsArticleRepository,
                       for_date: datetime.date | None = None,
                       market_indicators_max_value_count: int = 3,
                       stock_indicators_max_age: int = 3,
                       stock_values_max_age: int = 31,
                       max_news_age: int = 7,
                       max_news_count: int = 7,
                       ) -> str:
    """ Generates a GPT query for the given stock symbol.
    Args:
        symbol (str): The stock symbol to generate the query for.
        logger (logging.Logger): The logger to use
        news_repo (INewsArticleRepository): The repository to use for news articles
        stock_value_repo (IStockValueRepository): The repository to use for stock values
        stock_indicator_repo (IStockIndicatorRepository): The repository to use for stock indicators
        market_indicator_repo (IMarketIndicatorRepository): The repository to use for market indicators
        for_date (datetime.date, optional): The date to generate the query for.
                                            If `None`, the current date is used.
        market_indicators_max_value_count (int): The maximum number of market indicators to use (latest).
        stock_indicators_max_age (int): The maximum age of stock indicators to use in days.
        stock_values_max_age (int): The maximum age of stock values to use in days.
        max_news_age (int): The maximum age of news articles to use in days.
        max_news_count (int): The maximum number of news articles to use.
    """

    if for_date is None:
        for_date = datetime.date.today()

    # gather stock values
    logger.info(_("Gathering stock values for {symbol} (Code: 4823094)").format(symbol=symbol))
    symbol_data = stock_value_repo.get(symbol)
    if symbol_data is None:
        raise StockGptException(_("No data for symbol {symbol} (Code: 94823094)").format(symbol=symbol))

    relevant_stock_values = {
        **symbol_data.sample_two_values_per_month(for_date-datetime.timedelta(days=stock_values_max_age)),
        **symbol_data.get_values_for_date_range(
        date_from=for_date - datetime.timedelta(days=stock_values_max_age),
        date_to=for_date)
    }

    # gather market indicators
    logger.info(_("Gathering market indicators (Code: 203482394)"))
    relevant_market_indicators = {}
    for market_indicator in market_indicator_repo.list_keys():
        relevant_market_indicators[market_indicator] = {}
        vals = market_indicator_repo.get(market_indicator)
        for date, value in sorted(vals.items(), key=lambda x: x[0], reverse=True):
            if date > for_date:
                continue
            relevant_market_indicators[market_indicator][date] = value
            if len(relevant_market_indicators[market_indicator]) >= market_indicators_max_value_count:
                break

    # gather stock indicators
    logger.info(_("Gathering stock indicators for {symbol} (Code: 203482394)").format(symbol=symbol))
    stock_indicators = stock_indicator_repo.get(symbol)
    if stock_indicators is None:
        raise StockGptException(_("No stock indicators for symbol {symbol} (Code: 234234234)").format(symbol=symbol))

    relevant_stock_indicators = {}
    for date, stock_indicators in stock_indicators.items():
        if date > for_date or date < for_date - datetime.timedelta(days=stock_indicators_max_age):
            continue
        relevant_stock_indicators[date] = {}

        for stock_indicator, value in stock_indicators.items():
            relevant_stock_indicators[date][stock_indicator] = value

    logger.info(_("Fetching basic stock information for {symbol} (Code: 8203948)").format(symbol=symbol))
    info = fetch_basic_stock_info(symbol)
    logger.info(_("Fetching news for {symbol} (Code: 3423482)").format(symbol=symbol))
    relevant_news = []
    for article in news_repo.get(symbol) or []:
        date_news = datetime.date.fromtimestamp(article.published_at.timestamp())
        if for_date >= date_news >= (for_date - datetime.timedelta(days=max_news_age)):
            if article.title not in [x.title for x in relevant_news]: # don't add duplicates
                relevant_news.append(article)

    # shuffle and limit news
    shuffle(relevant_news)
    relevant_news = relevant_news[:max_news_count]

    query = "Today is: {}\n".format(for_date.strftime("%Y-%m-%d"))
    query += "The following description describes the stock `{symbol}` " \
             "including technical indicators, news, and general information:\n".format(symbol=symbol)
    #query += "We want to do an analysis and find a strategy for the stock `{symbol}`. All values considered to be in USD $.\n".format(
    #    symbol=symbol)
    query += "The following basic information is available:\n"
    for key, value in asdict(info).items():
        query += "- {}: {}\n".format(key.replace('_', ' '), value)
    query += "\n\n"
    query += "The stock progression in date: (open, high, low, close, volume); ... format is:\n"
    for date, stock_value in relevant_stock_values.items():
        date_str = date.strftime("%Y-%m-%d")

        query += "{date}: ({open:.2f},{high:.2f},{low:.2f},{close:.2f},{volume:}); ".format(
            open=stock_value.open,
            high=stock_value.high,
            low=stock_value.low,
            close=stock_value.close,
            volume=int(stock_value.volume) if not pd.isna(stock_value.volume) else 'unknown',
            date=date_str,
        )

    query += "\n\nSome market indicators in format: `market indicator name: " \
             "[(date: value), ...]` are given as follows: \n"
    for market_indicator, values in relevant_market_indicators.items():
        query += "- {}: [".format(market_indicator)
        for date, value in values.items():
            if value is not None:
                query += "({date}: {value:.2f}),".format(date=date.strftime("%Y-%m-%d"), value=value)
        query = query[:-1]
        query += "]\n"

    query += "\nSome stock related indicators in format: `date: [(stock indicator: value), ...]` " \
             "are given as follows: \n"

    for date, stock_indicators in relevant_stock_indicators.items():
        query += "- {}: [".format(date.strftime("%Y-%m-%d"))
        for stock_indicator, value in stock_indicators.items():
            query += "({stock_indicator}: {value:.2f}),".format(stock_indicator=stock_indicator,
                                                                value=value)

        query = query[:-1]
        query += "]\n"

    query += "\n\n"
    query += "The following news articles are available:\n"
    if len(relevant_news) == 0:
        query += "- No news available\n"

    for news_article in relevant_news:
        query += "- {date}: `{title}`\n{content}(Source: {source})\n".format(title=news_article.title,
                                                                               source=news_article.source,
                                                                               content='',# 'Content: ' + news_article.summary + '\n' or '',
                                                                               date=news_article.published_at.strftime(
                                                                           "%Y-%m-%d"))
    query += "\n\n"
    query += """
What are the bearish, neutral and bullish factors? Rate them in a scale (1 to 5 = important). Include the news headlines as appropriate. 
Conclude a short term investment strategy (max. 1 month) with buy signal, sell signal, rebuy signal and stop loss. 
If appropriate, that might be a shorting strategy as well. Estimate the success rate for a positive yield in a range from 1 to 10. 
"""
    return query
