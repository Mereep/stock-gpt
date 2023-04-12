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
# Brief: File Based implementation for NewsArticle Repository           #
#########################################################################
from __future__ import annotations

import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd

from datatypes.news_article import TNewsArticles, NewsArticle
from exceptions.repository import StockGptRepositoryException
from repository.news.i_news_article_repository import INewsArticleRepository

import gettext


class NewsArticleFileRepository(INewsArticleRepository):
    _base_path: Path

    def __init__(self, base_path: Path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not base_path.exists():
            raise StockGptRepositoryException(_('Base path {base_path} does not exist (Code: 428340923)'))

        self._base_path = base_path

    def get(self, key: str) -> TNewsArticles | None:
        news_article_base_path = self._base_path
        effective_path = news_article_base_path / f'{key}.csv'
        if effective_path.exists():
            df = pd.read_csv(effective_path, index_col=None, parse_dates=['published_at'])
            return TNewsArticles([NewsArticle(title=row['title'],
                                source=row['source'],
                                published_at=datetime.datetime.fromtimestamp(row['published_at'].timestamp()),
                                url=row['url'],
                                summary=row['summary'] if not pd.isna(row['summary']) else None)
                    for _, row in df.iterrows()])
        else:
            return None

    def store(self, key: str, value: TNewsArticles):
        _ = gettext.gettext
        news_article_base_path = self._base_path
        effective_path = news_article_base_path / f'{key}.csv'
        if not effective_path.exists():
            self.log_info(_('Creating new news article file for {key} (Code: 42342342)'))
            df_old = pd.DataFrame(columns=['title', 'source', 'published_at', 'url', 'summary'])
        else:
            self.log_info(_('Writing to existing news file {key} (Code: 2342834092)'))
            df_old = pd.read_csv(effective_path, index_col=None, parse_dates=['published_at'])

        df_new = pd.DataFrame({'title': [article.title for article in value],
                               'source': [article.source for article in value],
                               'published_at': [article.published_at for article in value],
                               'url': [article.url for article in value],
                               'summary': [article.summary for article in value]})

        # update or append
        for _, row_new in df_new.iterrows():
            if row_new['url'] in df_old['url'].values:
                df_old.loc[df_old['url'] == row_new['url']].iloc[0] = row_new.iloc[0]
            else:
                df_old = pd.concat([df_old, row_new.to_frame().T], axis=0, ignore_index=True)

        # sort by date
        df_old = df_old.sort_values(by=['published_at'])

        # save back to disk
        df_old.to_csv(effective_path, index=False)

    def list_keys(self) -> Iterable[str]:
        return [f.name.replace('.csv', '')
                for f in self._base_path.iterdir() if f.is_file() and f.name.endswith('.csv')]
