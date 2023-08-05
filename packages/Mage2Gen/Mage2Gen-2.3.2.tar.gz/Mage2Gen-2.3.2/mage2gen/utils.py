# A Magento 2 module generator library
# Copyright (C) 2016 Maikel Martens
#
# This file is part of Mage2Gen.
#
# Mage2Gen is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import string


class DefaultFormatter(string.Formatter):
	def __init__(self, default=''):
		self.default = default
	
	def get_field(self, field_name, args, kwargs):
		try:
			return super().get_field(field_name, args, kwargs)
		except (KeyError, AttributeError):
			return self.default

def upperfirst(word):
	return word[0].upper() + word[1:]

def lowerfirst(word):
	return word[0].lower() + word[1:]

