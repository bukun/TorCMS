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

__all__ = (
    'TornadoMeta',
)

from wtforms.meta import DefaultMeta
from .i18n import TornadoTranslations


class TornadoMeta(DefaultMeta):

    def get_translations(self, form):
        """
        Override in subclasses to provide alternate translations factory.
        See the i18n documentation for more.

        :param form: The form.
        :return: An object that provides gettext() and ngettext() methods.
        """
        if form.current_locale:
            return TornadoTranslations(form.current_locale)
        return None
