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

from collections.abc import Callable, Mapping
import re
from typing import Any

import jsonschema
import netaddr
from oslo_serialization import base64
from oslo_utils import timeutils
from oslo_utils import uuidutils
import rfc3986

from oslo_wsgi._i18n import _
from oslo_wsgi import exceptions

_FORMAT_CHECKER = jsonschema.FormatChecker()


@_FORMAT_CHECKER.checks('regex')  # type: ignore
def _validate_regex_format(instance: object) -> bool:
    # format checks constrain to the relevant primitive type
    # https://github.com/OAI/OpenAPI-Specification/issues/3148
    if not isinstance(instance, str):
        return True

    # the empty string is a valid regex but doesn't give us anything to match
    # on
    if not instance:
        return False

    try:
        re.compile(instance)
    except re.error:
        return False
    return True


@_FORMAT_CHECKER.checks('date-time')  # type: ignore
def _validate_datetime_format(instance: object) -> bool:
    # format checks constrain to the relevant primitive type
    # https://github.com/OAI/OpenAPI-Specification/issues/3148
    if not isinstance(instance, str):
        return True

    try:
        timeutils.parse_isotime(instance)
    except ValueError:
        return False
    else:
        return True


@_FORMAT_CHECKER.checks('base64')  # type: ignore
def _validate_base64_format(instance: object) -> bool:
    # format checks constrain to the relevant primitive type
    # https://github.com/OAI/OpenAPI-Specification/issues/3148
    if not isinstance(instance, str):
        return True

    try:
        if isinstance(instance, str):
            instance = instance.encode('utf-8')
        base64.decode_as_bytes(instance)
    except TypeError:
        # The name must be string type. If instance isn't string type, the
        # TypeError will be raised at here.
        return False

    return True


@_FORMAT_CHECKER.checks('cidr')  # type: ignore
def _validate_cidr_format(instance: object) -> bool:
    # format checks constrain to the relevant primitive type
    # https://github.com/OAI/OpenAPI-Specification/issues/3148
    if not isinstance(instance, str):
        return True

    try:
        netaddr.IPNetwork(instance)
    except netaddr.AddrFormatError:
        return False

    if '/' not in instance:
        return False

    if re.search(r'\s', instance):
        return False

    return True


@_FORMAT_CHECKER.checks('uuid')  # type: ignore
def _validate_uuid_format(instance: object) -> bool:
    # format checks constrain to the relevant primitive type
    # https://github.com/OAI/OpenAPI-Specification/issues/3148
    if not isinstance(instance, str):
        return True

    return uuidutils.is_uuid_like(instance)  # type: ignore


@_FORMAT_CHECKER.checks('uri')  # type: ignore
def _validate_uri(instance: object) -> bool:
    # format checks constrain to the relevant primitive type
    # https://github.com/OAI/OpenAPI-Specification/issues/3148
    if not isinstance(instance, str):
        return True

    uri = rfc3986.uri_reference(instance)
    validator = (
        rfc3986.validators.Validator()
        .require_presence_of(
            'scheme',
            'host',
        )
        .check_validity_of(
            'scheme',
            'userinfo',
            'host',
            'path',
            'query',
            'fragment',
        )
    )
    try:
        validator.validate(uri)
    except rfc3986.exceptions.RFC3986Exception:
        return False

    return True


_ValidatorT = Callable[..., bool]


class _SchemaValidator:
    """Base validator class

    A superset of Draft202012Validator that includes support for our custom
    format types.
    """

    validator_org = jsonschema.Draft202012Validator

    def __init__(
        self,
        schema: dict[str, Any],
        *,
        validators: Mapping[str, _ValidatorT] | None = None,
    ) -> None:
        validator_cls = jsonschema.validators.extend(
            self.validator_org, validators
        )
        self.validator = validator_cls(schema, format_checker=_FORMAT_CHECKER)

    def validate(self, instance: Any) -> None:
        try:
            self.validator.validate(instance)
        except jsonschema.ValidationError as ex:
            if len(ex.path) > 0:
                # NOTE: For whole OpenStack message consistency, this error
                # message has been written as the similar format of WSME.
                message = _(
                    'Invalid input for field/attribute %(path)s. '
                    'Value: %(value)s. %(message)s'
                ) % {
                    'path': ex.path.pop(),
                    'value': ex.instance,
                    'message': ex.message,
                }
            else:
                message = ex.message
            raise exceptions.ValidationError(message)
        except TypeError as ex:
            # NOTE: If passing non string value to patternProperties parameter,
            #       TypeError happens. Here is for catching the TypeError.
            message = str(ex)
            raise exceptions.ValidationError(message)
