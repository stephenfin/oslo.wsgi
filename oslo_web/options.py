# Copyright 2015 Mirantis Inc.
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

import copy

from oslo_config import cfg

paste_opts: list[cfg.Opt] = [
    cfg.StrOpt(
        'api_paste_config',
        default='api-paste.ini',
        help='File name for the paste.deploy config for api service',
    ),
]

validation_opts: list[cfg.Opt] = [
    cfg.StrOpt(
        'response_validation',
        choices=(
            (
                'error',
                'Raise a HTTP 500 (Server Error) for responses that fail '
                'response body schema validation',
            ),
            (
                'warn',
                'Log a warning for responses that fail response body schema '
                'validation',
            ),
            (
                'ignore',
                'Ignore response body schema validation failures',
            ),
        ),
        default='warn',
        help="""\
Configure validation of API responses.


``warn`` is the current recommendation for production environments. ``error``
should only be used in testing environments.

If you find it necessary to enable the ``ignore`` option, please report the
issues you are seeing so we can improve our schemas.
""",
    ),
]


def register_opts(conf: cfg.ConfigOpts) -> None:
    """Registers WSGI config options."""
    conf.register_opts(paste_opts, 'api')
    conf.register_opts(validation_opts, 'api')


def list_opts() -> list[tuple[str | None, list[cfg.Opt]]]:
    """Return a list of oslo.config options available in the library.

    The returned list includes all oslo.config options which may be registered
    at runtime by the library.

    Each element of the list is a tuple. The first element is the name of the
    group under which the list of elements in the second element will be
    registered. A group name of None corresponds to the [DEFAULT] group in
    config files.

    This function is also discoverable via the 'oslo_wsgi' entry point under
    the 'oslo.config.opts' namespace.

    The purpose of this is to allow tools like the Oslo sample config file
    generator to discover the options exposed to users by this library.

    :returns: a list of (group_name, opts) tuples
    """
    return [
        ('api', copy.deepcopy(paste_opts) + copy.deepcopy(validation_opts))
    ]
