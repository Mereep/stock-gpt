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
# Brief: Implementation for Indicator-Extractors                        #
# Most of the indicators are implemented using the TA-Lib library       #
# and written by ChatGPT ;)
#########################################################################

import datetime

import numpy as np
import talib

from datatypes.stock_data import StockDataInfo
from stock_indicators.i_indicator import IStockIndicator


class SMA50(IStockIndicator):
    @staticmethod
    def id():
        return "SMA50"

    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        closes = data.filter_close_dates_until(until_date=for_date)
        return talib.SMA(np.array(closes), timeperiod=50)[-1]


class SMA200(IStockIndicator):
    @staticmethod
    def id():
        return "SMA200"

    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        closes = data.filter_close_dates_until(for_date)
        return talib.SMA(np.array(closes), timeperiod=200)[-1]


class EMA50(IStockIndicator):
    @staticmethod
    def id():
        return "EMA50"

    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        closes = data.filter_close_dates_until(for_date)
        return talib.EMA(np.array(closes), timeperiod=50)[-1]


class EMA200(IStockIndicator):
    @staticmethod
    def id():
        return "EMA200"

    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        closes = data.filter_close_dates_until(for_date)
        return talib.EMA(np.array(closes), timeperiod=200)[-1]


class RSI(IStockIndicator):
    @staticmethod
    def id():
        return "RSI"

    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        closes = data.filter_close_dates_until(for_date)
        return talib.RSI(np.array(closes))[-1]


class MACD(IStockIndicator):
    @staticmethod
    def id():
        return "MACD"

    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        closes = data.filter_close_dates_until(for_date)
        macd, _, _ = talib.MACD(np.array(closes))
        return macd[-1]


class MACDSignal(IStockIndicator):
    @staticmethod
    def id():
        return "MACD_Signal"

    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        closes = data.filter_close_dates_until(for_date)
        _, macd_signal, _ = talib.MACD(np.array(closes))
        return macd_signal[-1]


class MACDHist(IStockIndicator):
    @staticmethod
    def id():
        return "MACD_Hist"

    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        closes = data.filter_close_dates_until(for_date)
        _, _, macd_hist = talib.MACD(np.array(closes))
        return macd_hist[-1]


class BbUpper(IStockIndicator):
    @staticmethod
    def id():
        return "BB_Upper"

    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        closes = data.filter_close_dates_until(for_date)
        upper, _, _ = talib.BBANDS(np.array(closes))
        return upper[-1]


class BbMiddle(IStockIndicator):
    @staticmethod
    def id():
        return "BB_Middle"

    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        closes = data.filter_close_dates_until(for_date)
        _, middle, _ = talib.BBANDS(np.array(closes))
        return middle[-1]


class BbLower(IStockIndicator):
    @staticmethod
    def id():
        return "BB_Lower"

    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        closes = data.filter_close_dates_until(for_date)
        _, _, lower = talib.BBANDS(np.array(closes))
        return lower[-1]


class SoSlowK(IStockIndicator):
    @staticmethod
    def id():
        return "SO_SlowK"

    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        high_prices = data.filter_high_dates_until(for_date)
        low_prices = data.filter_low_dates_until(for_date)
        closes = data.filter_close_dates_until(for_date)
        slowk, _ = talib.STOCH(np.array(high_prices),
                               np.array(low_prices),
                               np.array(closes))
        return slowk[-1]


class SoSlowD(IStockIndicator):
    @staticmethod
    def id():
        return "SO_SlowD"

    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        high_prices = data.filter_high_dates_until(for_date)
        low_prices = data.filter_low_dates_until(for_date)
        closes = data.filter_close_dates_until(for_date)
        _, slowd = talib.STOCH(np.array(high_prices), np.array(low_prices), np.array(closes))

        return slowd[-1]


class ADX(IStockIndicator):
    @staticmethod
    def id():
        return "ADX"

    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        high_prices = data.filter_high_dates_until(for_date)
        low_prices = data.filter_low_dates_until(for_date)
        closes = data.filter_close_dates_until(for_date)

        return talib.ADX(np.array(high_prices), np.array(low_prices), np.array(closes))[-1]


class AroonOscillator(IStockIndicator):
    @staticmethod
    def id():
        return "Aroon_Oscillator"

    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        high_prices = data.filter_high_dates_until(for_date)
        low_prices = data.filter_low_dates_until(for_date)
        aroon_up, aroon_down = talib.AROON(np.array(high_prices), np.array(low_prices))
        aroon_oscillator = aroon_up - aroon_down

        return aroon_oscillator[-1]


class OBV(IStockIndicator):
    @staticmethod
    def id():
        return "OBV"

    def calculate(self, data: StockDataInfo, for_date: datetime.date) -> float:
        closes = data.filter_close_dates_until(for_date)
        volumes = data.filter_volumes_dates_until(for_date)
        return talib.OBV(np.array(closes, dtype=np.float64),
                         np.array(volumes, dtype=np.float64))[-1]
