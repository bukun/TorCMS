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

__all__ = (
    'TornadoInputWrapper',
    'TornadoForm',
)

import warnings

from tornado import escape
from wtforms import form

from .meta import TornadoMeta


class TornadoInputWrapper(object):
    def __init__(self, multidict):
        self._wrapped = multidict

    def __iter__(self):
        return iter(self._wrapped)

    def __len__(self):
        return len(self._wrapped)

    def __contains__(self, name):
        return name in self._wrapped

    def __getitem__(self, name):
        return self._wrapped[name]

    def __getattr__(self, name):
        return self.__getitem__(name)

    def getlist(self, name):
        try:
            return [escape.to_unicode(v) for v in self._wrapped[name]]
        except KeyError:
            return []


class TornadoForm(form.Form):
    """
    A Form derivative which uses the locale module from Tornado.
    """

    Meta = TornadoMeta

    def __init__(
        self,
        formdata=None,
        obj=None,
        prefix="",
        data=None,
        meta=None,
        **kwargs,
    ):
        self._locale_code = kwargs.get("locale_code", "en_US")
        super(TornadoForm, self).__init__(
            formdata=formdata, obj=obj, prefix=prefix, data=data, meta=meta, **kwargs
        )

    @property
    def current_locale(self):
        return self._locale_code

    def process(self, formdata=None, obj=None, **kwargs):
        if formdata is not None and not hasattr(formdata, 'getlist'):
            formdata = TornadoInputWrapper(formdata)
        super(TornadoForm, self).process(formdata, obj, **kwargs)


class Form(TornadoForm):
    def __init__(
        self, formdata=None, obj=None, prefix="", data=None, meta=None, **kwargs
    ):
        warnings.warn(
            "The tornado_wtforms.form.Form class is depreciated, please use "
            "tornado_wtforms.form.TornadoForm.",
            DeprecationWarning,
            stacklevel=3,
        )
        super(Form, self).__init__(
            formdata=formdata, obj=obj, prefix=prefix, data=data, meta=meta, **kwargs
        )
