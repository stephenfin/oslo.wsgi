# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# Copyright 2010 OpenStack Foundation
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

from oslo_log import log as logging
from paste import deploy

from oslo_web import exceptions
from oslo_web import options

LOG = logging.getLogger(__name__)


class Loader:
    """Used to load WSGI applications from paste configurations."""

    def __init__(self, conf):
        """Initialize the loader, and attempt to find the config.

        :param conf: Application config
        :returns: None

        """
        conf.register_opts(options.opts)
        self.config_path = None

        config_path = conf.api_paste_config
        if not os.path.isabs(config_path):
            self.config_path = conf.find_file(config_path)
        elif os.path.exists(config_path):
            self.config_path = config_path

        if not self.config_path:
            raise exceptions.ConfigNotFound(path=config_path)

    def load_app(self, name):
        """Return the paste URLMap wrapped WSGI application.

        :param name: Name of the application to load.
        :returns: Paste URLMap object wrapping the requested application.
        :raises: PasteAppNotFound

        """
        try:
            LOG.debug(
                'Loading app %(name)s from %(path)s',
                {'name': name, 'path': self.config_path},
            )
            return deploy.loadapp(f'config:{self.config_path}', name=name)
        except LookupError:
            LOG.exception("Couldn't lookup app: %s", name)
            raise exceptions.PasteAppNotFound(name=name, path=self.config_path)
