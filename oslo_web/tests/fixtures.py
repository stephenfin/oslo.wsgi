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

import warnings

import fixtures


class WarningsFixture(fixtures.Fixture):
    """Filters out warnings during test runs."""

    def setUp(self):
        super().setUp()

        self._original_warning_filters = warnings.filters[:]

        warnings.simplefilter('once', DeprecationWarning)

        # we don't use the PkgResourcesParser parser from paste.urlparser
        # remove this once setuptools > 80.9.0 is released, which will remove
        # the pkg_resources package
        warnings.filterwarnings(
            'ignore',
            message='pkg_resources is deprecated as an API',
            module='paste.urlparser',
            category=UserWarning,
        )

        self.addCleanup(self._reset_warning_filters)

    def _reset_warning_filters(self):
        warnings.filters[:] = self._original_warning_filters  # type: ignore[index]
