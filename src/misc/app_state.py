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
# Brief: Globally available AppState                                    #
# (rather use DI, though where possible)                             	#
#########################################################################
from misc.config import AppConfig

app_config = AppConfig.from_env()


def get_app_config() -> AppConfig:
    """Get the global app configuration"""
    return app_config
