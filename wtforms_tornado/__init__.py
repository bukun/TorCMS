# -*- coding: UTF-8 -*-
#
# Copyright 2022 Flávio Gonçalves Garcia
# Copyright 2013-2022 Jorge Puente Sarrín
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings

version_tuple = (0, 0, 2)


def get_version_string():
    if isinstance(version_tuple[-1], str):
        return '.'.join(map(str, version_tuple[:-1])) + version_tuple[-1]
    return '.'.join(map(str, version_tuple))


version = get_version_string()
"""Current version of wtforms-tornado."""


__author__ = 'Jorge Puente Sarrín <puentesarrin@gmail.com>'
__since__ = '2013-09-25'
__version__ = version

warnings.warn("Importing from wtforms_tornado is depreciated, please utilize "
              "tornado_wtforms.", DeprecationWarning, stacklevel=2)

from tornado_wtforms.form import Form
