# -*- coding: UTF-8 -*-
#
# Copyright 2022 Flávio Gonçalves Garcia
# Copyright 2013-2014 Jorge Puente Sarrín
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

__author__ = "Flávio Gonçalves Garcia <piraz@candango.org>"
__version__ = (0, 0, 1)
__licence__ = "Apache License V2.0"


def get_version():
    if isinstance(__version__[-1], str):
        return '.'.join(map(str, __version__[:-1])) + __version__[-1]
    return ".".join(map(str, __version__))


def get_author():
    return __author__.split(" <")[0]


def get_author_email():
    return __author__.split(" <")[1][:-1]
