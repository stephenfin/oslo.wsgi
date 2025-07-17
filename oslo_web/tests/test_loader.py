# Copyright 2011 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import tempfile
from unittest import mock

from oslo_config import cfg

from oslo_web import exceptions
from oslo_web import loader
from oslo_web.tests import base

CONF = cfg.CONF


class TestLoaderNothingExists(base.BaseTestCase):
    """Loader tests where os.path.exists always returns False."""

    def setUp(self):
        super().setUp()

        mock_patcher = mock.patch.object(os.path, 'exists', lambda _: False)
        mock_patcher.start()
        self.addCleanup(mock_patcher.stop)

    def test_relpath_config_not_found(self):
        self.config(api_paste_config='api-paste.ini')
        self.assertRaises(exceptions.ConfigNotFound, loader.Loader, self.conf)

    def test_asbpath_config_not_found(self):
        self.config(api_paste_config='/etc/openstack-srv/api-paste.ini')
        self.assertRaises(exceptions.ConfigNotFound, loader.Loader, self.conf)


class TestLoaderNormalFilesystem(base.BaseTestCase):
    """Loader tests with normal filesystem (unmodified os.path module)."""

    _paste_config = """
[app:test_app]
use = egg:Paste#static
document_root = /tmp
    """

    def setUp(self):
        super().setUp()
        self.paste_config = tempfile.NamedTemporaryFile(mode='w+t')
        self.paste_config.write(self._paste_config.lstrip())
        self.paste_config.seek(0)
        self.paste_config.flush()

        self.config(api_paste_config=self.paste_config.name)
        self.loader = loader.Loader(CONF)

    def tearDown(self):
        self.paste_config.close()
        super().tearDown()

    def test_config_found(self):
        self.assertEqual(self.paste_config.name, self.loader.config_path)

    def test_app_not_found(self):
        self.assertRaises(
            exceptions.PasteAppNotFound,
            self.loader.load_app,
            'nonexistent app',
        )

    def test_app_found(self):
        url_parser = self.loader.load_app('test_app')
        self.assertEqual('/tmp', url_parser.directory)
