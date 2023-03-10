#!/usr/bin/env python
#
# Copyright 2013 Stoneopus
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""A lightweight wrapper around psycopg2.
补充说明：代码来自于 https://github.com/markgao/tornpg
针对 PostGIS 可能会有较多修改，故把源代码直接放在这里。
"""

from __future__ import absolute_import, division, with_statement

import copy
import itertools
import logging
import os
import time

try:
    import psycopg2
    import psycopg2.extensions
    from psycopg2.extensions import (connection as base_connection,
                                     cursor as base_cursor)
except ImportError:
    # If psycopg2 isn't available this module won't actually be useable,
    # but we want it to at least be importable on readthedocs.org,
    # which has limitations on third-party modules.
    if 'READTHEDOCS' in os.environ:
        psycopg2 = None
    else:
        raise

version = "0.1"
version_info = (0, 1, 2, 0)

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)


class Connection(object):
    """A lightweight wrapper around psycopg2 DB-API connections.

    The main value we provide is wrapping rows in a dict/object so that
    columns can be accessed by name. Typical usage::

        db = database.Connection("127.0.0.1", "mydb")
        for fish in db.query("SELECT * FROM fishes"):
            print fish.name

    Cursors are hidden by the implementation, but other than that, the methods
    are very similar to the DB-API.

    --We explicitly set the timezone to UTC and the character encoding to
    --UTF-8 on all connections to avoid time zone and encoding errors.
    """

    def __init__(self, host, database, port=None, user=None, password=None,
                 max_idle_time=2 * 3600, connect_timeout=0,
                 connection_factory=None):
        self.host = host
        self.database = database
        self.max_idle_time = float(max_idle_time)

        args = dict(client_encoding="utf8", database=database,
                    connect_timeout=connect_timeout)
        if user is not None:
            args['user'] = user
        if password is not None:
            args['password'] = password

        # We accept a path to a host(:port) string
        pair = host.split(":")
        if len(pair) == 2:
            args['host'] = pair[0]
            args['port'] = port or int(pair[1])
        else:
            args['host'] = host
            args['port'] = port or 5432

        args['connection_factory'] = \
            connection_factory or base_connection

        self._db = None
        self._db_args = args
        self._last_use_time = time.time()
        try:
            self.reconnect()
        except Exception:
            logging.error("Cannot connect to Postgresql on %s:%s", self.host,
                          exc_info=True)

    def __del__(self):
        self.close()

    def close(self):
        """Closes this database connection."""
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def reconnect(self):
        """Closes the existing database connection and re-opens it."""
        self.close()
        self._db = psycopg2.connect(**self._db_args)
        # It's not a good idea to autocommit
        # self._db.autocommit = True

    def commit(self):
        """Commit any pending transaction to the database.
        By default, Psycopg opens a transaction before executing the first
        command: if commit() is not called, the effect of any data
        manipulation will be lost.

        The connection can be also set in "autocommit" mode: no transaction
        is automatically open, commands have immediate effect.
        """
        return self._db.commit()

    def rollback(self):
        """Roll back to the start of any pending transaction. Closing a
        connection without committing the changes first will cause an implicit
        rollback to be performed.
        Changed in psycopg2 version 2.5: if the connection is used in a with
        statement, the method is automatically called if an exception is raised
        in the with block.
        """
        return self._db.rollback()

    def query(self, query, *parameters, **kwparameters):
        """Returns a row list for the given query and parameters."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kwparameters)
            column_names = [d[0] for d in cursor.description]
            return [Row(itertools.izip(column_names, row)) for row in cursor]
        finally:
            cursor.close()

    def get(self, query, *parameters, **kwparameters):
        """Returns the (singular) row returned by the given query.

        If the query has no results, returns None. If it has
        more than one result, raises an exception.
        """
        rows = self.query(query, *parameters, **kwparameters)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            return rows[0]

    # rowcount is a more reasonable default return value than lastrowid,
    # but for historical compatibility execute() must return lastrowid.
    def execute(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the lastrowid from the query."""
        return self.execute_lastrowid(query, *parameters, **kwparameters)

    def execute_lastrowid(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the lastrowid from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kwparameters)
            return cursor.fetchone()[0]
        finally:
            cursor.close()

    def execute_rowcount(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the rowcount from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kwparameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def executemany(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the lastrowid from the query.
        """
        return self.executemany_lastrowid(query, parameters)

    def executemany_lastrowid(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the lastrowid from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def executemany_rowcount(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the rowcount from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    update = execute_rowcount
    updatemany = executemany_rowcount

    insert = execute_lastrowid
    insertmany = executemany_lastrowid

    def _ensure_connected(self):
        # Postgresql by default closes client connections that are idle for
        # 2 hours on linux, but the client library does not report this fact
        # until you try to perform a query and it fails.  Protect against
        # this case by preemptively closing and reopening the connection
        # if it has been idle for too long (7 hours by default).
        if (self._db is None or
                (time.time() - self._last_use_time > self.max_idle_time)):
            self.reconnect()
        self._last_use_time = time.time()

    def _cursor(self):
        self._ensure_connected()
        return self._db.cursor()

    def _execute(self, cursor, query, parameters, kwparameters):
        try:
            return cursor.execute(query, kwparameters or parameters)
        except OperationalError:
            logging.error("Error connecting to Postgresql on %s", self.host)
            self.close()
            raise


class Row(dict):
    """A dict that allows for object-like property access syntax."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


IntegrityError = psycopg2.IntegrityError
OperationalError = psycopg2.OperationalError
