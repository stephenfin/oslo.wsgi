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

from oslo_web._i18n import _


class ConfigNotFound(Exception):
    def __init__(self, path: str) -> None:
        msg = _('Could not find config at %(path)s') % {'path': path}
        super().__init__(msg)


class PasteAppNotFound(Exception):
    def __init__(self, name: str, path: str) -> None:
        msg = _("Could not load paste app '%(name)s' from %(path)s") % {
            'name': name,
            'path': path,
        }
        super().__init__(msg)


class ValidationError(Exception):
    """Base class for validation failures."""
