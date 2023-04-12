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
# Brief: CLI interface for library                                      #
#########################################################################
import argparse
import datetime
import gettext

from cli.commands import update_market_indicator_data, update_stock_symbol_data, update_stock_indicator_data, \
    update_news_data, generate_query
from log.logger import get_default_cli_logger
from misc.app_state import get_app_config
from repository.market_indicator.market_indicator_file_repository import MarketIndicatorFileRepository
from repository.news.news_article_file_repository import NewsArticleFileRepository
from repository.stock_indicator.stock_indicator_file_repository import StockIndicatorFileRepository
from repository.stock_value.stock_value_file_repository import StockValueFileRepository

_ = gettext.gettext


def parse_arguments():
    """
    Parse command line arguments and return the parsed arguments.
    """
    app_config = get_app_config()
    parser = argparse.ArgumentParser(
        description=_("Stock market summary interface to use with ChatGPT and friends"))
    toplevel_parser = parser.add_subparsers(
        title=_("Base commands"), dest='command')

    symbol_command = toplevel_parser.add_parser('symbols', help=_("Collect data"))

    symbol_subcommands = symbol_command.add_subparsers(dest='symbol_command')
    collect_parser = symbol_subcommands.add_parser('collect',
                                                   help=_("Collect charts symbols"))

    collect_parser.add_argument('--symbol',
                                required=False,
                                nargs='+',
                                type=str,
                                help=_("Symbol to collect data for. If None is given, all symbols are update"))

    collect_parser.add_argument('--start',
                                type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d').date(),
                                default=datetime.date.today() - datetime.timedelta(days=365),
                                help=_("Start date in YYYY-MM-DD format (default: today - 365 days)"))

    collect_parser.add_argument('--end',
                                type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d').date(),
                                default=datetime.date.today(),
                                help=_("End date in YYYY-MM-DD format (default: today)"))

    market_indicator_command = toplevel_parser.add_parser('market-indicators', help=_("Collect market indicators"))

    market_indicator_command.add_argument('--start',
                                          type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d').date(),
                                          default=None,
                                          help=_("Start date in YYYY-MM-DD format (default: None)"))

    market_indicator_command.add_argument('--end',
                                          type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d').date(),
                                          default=None,
                                          help=_("End date in YYYY-MM-DD format (default: None)"))

    market_indicator_subparsers = market_indicator_command.add_subparsers(dest='indicator_command')
    indicator_collect = market_indicator_subparsers.add_parser('update', help=_("Collect market indicators"))
    indicator_collect.add_argument('--indicator', nargs='+',
                                   type=str,
                                   default=app_config.default_market_indicators,
                                   help=_("List of indicators to collect data for (defaults to: {indicators}). "
                                          "See readme.md for descriptions").format(
                                       indicators=app_config.default_market_indicators))
    news_command = toplevel_parser.add_parser('news', help=_("Collect news data"))
    news_subcommands = news_command.add_subparsers(dest='news_command')
    news_update_parser = news_subcommands.add_parser('update', help=_("Update news data"))
    news_update_parser.add_argument('--symbol',
                                    required=False,
                                    nargs='+',
                                    type=str,
                                    help=_("List of symbols to collect news for. "
                                           "If None is given, all symbols are updated."))
    news_update_parser.add_argument('--page-size',
                                    required=False,
                                    type=int,
                                    default=15,
                                    help=_("Number of news articles to collect per symbol."))
    stock_indicators_parser = toplevel_parser.add_parser('stock-indicators', help=_("Calculate stock indicators"))
    stock_indicators_update_parser = stock_indicators_parser.add_subparsers(dest='stock_indicator_command')
    stock_indicators_update_parser.add_parser('update', help=_("Update stock indicators"))

    # Add the new 'query' command
    query_command = toplevel_parser.add_parser('query',
                                               help=_("Generate a ChatGPT query"))
    query_subcommands = query_command.add_subparsers(dest='query_command')

    # Add the 'generate' subcommand
    generate_parser = query_subcommands.add_parser('generate', help=_("Generate a ChatGPT query"))

    generate_parser.add_argument('--symbol',
                                 type=str,
                                 required=True,
                                 help=_("Symbol to generate the query for"))

    generate_parser.add_argument('--market_indicators_max_value_count',
                                 type=int,
                                 default=3,
                                 help=_("Maximum number of market indicator values to consider (default: 3)"))

    generate_parser.add_argument('--stock_indicators_max_age',
                                 type=int,
                                 default=3,
                                 help=_("Maximum age of stock indicators in days (default: 3)"))

    generate_parser.add_argument('--stock_values_max_age',
                                 type=int,
                                 default=31,
                                 help=_("Maximum age of stock values in days (default: 31)"))

    generate_parser.add_argument('--max_news_age',
                                 type=int,
                                 default=7,
                                 help=_("Maximum age of news articles in days (default: 7)"))

    generate_parser.add_argument('--day',
                                 type=lambda d: datetime.datetime.strptime(d, '%Y-%m-%d').date(),
                                 default=datetime.date.today(),
                                 help=_("Date in YYYY-MM-DD format for the query (default: today)"))

    generate_parser.add_argument('--update-symbol',
                                 action='store_true',
                                 help=_("Update symbol data before generating the query"))

    return parser.parse_args()


def main():
    args = parse_arguments()
    logger = get_default_cli_logger()
    if args.command == 'market-indicators':
        if args.indicator_command == 'update':
            update_market_indicator_data(
                app_config=get_app_config(),
                repo=MarketIndicatorFileRepository(base_path=get_app_config().market_indicator_base_dir,
                                                   logger=get_default_cli_logger()),
                logger=get_default_cli_logger(),
                indicators=args.indicator,
                from_date=args.start,
                to_date=args.end
            )
    elif args.command == 'symbols':
        if args.symbol_command == 'collect':
            repo = StockValueFileRepository(base_path=get_app_config().stock_value_base_dir,
                                            logger=logger)
            if args.symbol is None:
                symbols = repo.list_keys()
                logger.info(_("Updating all symbols: {symbols} (Code: 2482903)")
                            .format(symbols=symbols))
            else:
                symbols = args.symbol

            for symbol in symbols:
                update_stock_symbol_data(
                    repo=repo,
                    logger=logger,
                    symbol=symbol,
                    from_date=args.start,
                    to_date=args.end
                )

    elif args.command == 'stock-indicators':
        if args.stock_indicator_command == 'update':
            update_stock_indicator_data(
                stock_value_repo=StockValueFileRepository(base_path=get_app_config().stock_value_base_dir,
                                                          logger=logger),
                stock_indicator_repo=StockIndicatorFileRepository(base_path=get_app_config().stock_indicators_base_dir,
                                                                  logger=logger),
                indicators_to_update=get_app_config().default_stock_indicators,
                logger=get_default_cli_logger(),
            )

    elif args.command == 'news':
        if args.news_command == 'update':
            symbols = args.symbol
            if not symbols:
                repo_stock_value = StockValueFileRepository(base_path=get_app_config().stock_value_base_dir,
                                                            logger=logger)
                symbols = repo_stock_value.list_keys()

            for symbol in symbols:
                update_news_data(
                    repo=NewsArticleFileRepository(base_path=get_app_config().default_news_article_base_dir,
                                                   logger=get_default_cli_logger()),
                    symbol=symbol,
                    news_api_key=get_app_config().news_api_key,
                    logger=get_default_cli_logger(),
                    page_size=args.page_size,
                )

    if args.command == 'query' and args.query_command == 'generate':
        today = datetime.date.today()
        if args.day > today:
            logger.error(_("The specified date is in the future. "
                           "Please provide a date that is not in the future."))
            exit(1)
        else:
            market_indicator_repo = MarketIndicatorFileRepository(base_path=get_app_config().market_indicator_base_dir,
                                                                  logger=logger)

            stock_indicator_repo = StockIndicatorFileRepository(base_path=get_app_config().stock_indicators_base_dir,
                                                                logger=logger)

            symbol_value_repo = StockValueFileRepository(base_path=get_app_config().stock_value_base_dir,
                                                         logger=logger)

            news_repo = NewsArticleFileRepository(base_path=get_app_config().default_news_article_base_dir,
                                                  logger=logger)

            generate_query(
                market_indicator_repo=market_indicator_repo,
                stock_indicator_repo=stock_indicator_repo,
                stock_value_repo=symbol_value_repo,
                news_repo=news_repo,
                logger=logger,
                symbol=args.symbol,
                market_indicators_max_value_count=args.market_indicators_max_value_count,
                stock_indicators_max_age=args.stock_indicators_max_age,
                stock_values_max_age=args.stock_values_max_age,
                max_news_age=args.max_news_age,
                day=args.day,
                update_stock_symbol=args.update_symbol,
                news_api_key=get_app_config().news_api_key,
                stock_indicators_to_update=get_app_config().default_stock_indicators,
            )


if __name__ == '__main__':
    main()
