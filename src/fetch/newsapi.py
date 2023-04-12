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
# Brief: Functions to fetch from the NewsAPI                      		#
#########################################################################
from __future__ import annotations

import datetime

import requests

from datatypes.news_article import NewsArticle, TNewsArticles
from exceptions.base import StockGptException


def fetch_latest_stock_news(stock_symbol: str,
                            api_key: str,
                            page: int = 1,
                            stock_name: str | None=None,
                            page_size: int = 15
                            ) -> TNewsArticles:
    # Set up the endpoint and parameters
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': f'({stock_symbol} stock)'+f' OR {stock_name}' if stock_name else '',
        'sortBy': 'publishedAt',
        'apiKey': api_key,
        'language': 'en',
        'pageSize': page_size,
        'page': page,
    }

    # Send the request and parse the response
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data['articles']

        # Transform articles into NewsArticle dataclass instances
        news_articles = [
            NewsArticle(
                title=article['title'],
                source=article['source']['name'],
                published_at=datetime.datetime.fromisoformat(article['publishedAt']),
                url=article['url'],
                summary=article['content'] or article['description'],
            )
            for article in articles
        ]

        return TNewsArticles(news_articles)
    else:
        raise StockGptException(f"Couldn't fetch news data due to: {response.status_code} {response.text} "
                                f"(Code: 0482930482)")

