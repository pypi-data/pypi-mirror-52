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
import os
from . import Module, Phpclass, Phpmethod, Xmlnode, StaticFile, Snippet, SnippetParam
from ..utils import upperfirst

class UiComponentSnippet(Snippet):
	snippet_label = 'Ui Component'
	description = """
		Generates a basic ui component
	"""

	def add(self, test_suite, test_name, extra_params=None):
		class_name = "\\Test\\Unit\\{}Test".format(test_suite)

		unittest_class = Phpclass(class_name,extends='\\PHPUnit_Framework_TestCase')

		# Adding class setup and teardown
		unittest_class.add_method(
			Phpmethod(
				'setUpBeforeClass',
				access='public static',
				body="//setup",
				docstring=['Is called once before running all test in class']
			)
		)

		self.add_class(unittest_class)

	@classmethod
	def params(cls):
		return [
			SnippetParam(
				name='test_suite',
				description='Example: BlogPost',
				required=True, 
				regex_validator= r'^[a-zA-Z]{1}\w+$',
				error_message='Only alphanumeric and underscore characters are allowed, and need to start with a alphabetic character.',
				repeat=True),
			SnippetParam(
				name='test_name',
				description='Example: create',
				required=True, 
				regex_validator= r'^[a-zA-Z]{1}\w+$',
				error_message='Only alphanumeric and underscore characters are allowed, and need to start with a alphabetic character.'),
		]


