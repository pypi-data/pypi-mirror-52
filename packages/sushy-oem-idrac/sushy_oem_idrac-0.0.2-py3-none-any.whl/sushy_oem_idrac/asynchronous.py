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

from datetime import datetime
from datetime import timedelta
import logging
import time

from dateutil import parser
import sushy

LOG = logging.getLogger(__name__)


def _to_datetime(retry_after_str):
    if retry_after_str.isdigit():
        # Retry-After: 120
        return datetime.now() + timedelta(seconds=int(retry_after_str))
    else:
        # Retry-After: Fri, 31 Dec 1999 23:59:59 GMT
        return parser.parse(retry_after_str)


def http_call(conn, method, *args, **kwargs):
    handle = getattr(conn, method.lower())

    response = handle(*args, **kwargs)

    while response.status_code == 202:
        location = response.headers.get('location')
        if not location:
            raise sushy.exceptions.ExtensionError(
                error='Response %d to HTTP %s with args %s, kwargs %s '
                      'does not include Location: in '
                      'header' % (response.status_code, method.upper(),
                                  args, kwargs))

        retry_after = response.headers.get('retry-after')
        if retry_after:
            retry_after = _to_datetime(retry_after)
            sleep_for = max(0, (retry_after - datetime.now()).total_seconds())

        else:
            sleep_for = 60

        time.sleep(sleep_for)

        response = conn.get(location)

    if response.status_code >= 400:
        raise sushy.exceptions.ExtensionError(
            error='HTTP %s with args %s, kwargs %s failed '
                  'with code %s' % (method.upper(), args, kwargs,
                                    response.status_code))

    return response
