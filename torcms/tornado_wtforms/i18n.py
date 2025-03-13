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

from tornado import locale


class TornadoTranslations(object):
    """
    A translations object for WTForms that gets its messages from Tornado's
    locale module.
    """

    def __init__(self, code):
        self.locale = locale.get(code)

    def gettext(self, string):
        return self.locale.translate(string)

    def ngettext(self, singular, plural, n):
        return self.locale.translate(singular, plural, n)
