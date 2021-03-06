# Copyright 2013 IBM Corp.
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

from nova.compute import api as compute_api
from nova.tests.functional.v3 import test_servers
from nova.tests.unit.image import fake


class PreserveEphemeralOnRebuildJsonTest(test_servers.ServersSampleBase):
    extension_name = 'os-preserve-ephemeral-rebuild'

    def _test_server_rebuild_preserve_ephemeral(self, value):
        uuid = self._post_server()
        image = fake.get_valid_image_id()
        subs = {'host': self._get_host(),
                'uuid': image,
                'name': 'foobar',
                'pass': 'seekr3t',
                'hostid': '[a-f0-9]+',
                'preserve_ephemeral': str(value).lower(),
                'action': 'rebuild',
                'glance_host': self._get_glance_host(),
                }

        def fake_rebuild(self_, context, instance, image_href, admin_password,
                         files_to_inject=None, **kwargs):
            self.assertEqual(kwargs['preserve_ephemeral'], value)
        self.stubs.Set(compute_api.API, 'rebuild', fake_rebuild)

        response = self._do_post('servers/%s/action' % uuid,
                                 'server-action-rebuild-preserve-ephemeral',
                                 subs)
        self.assertEqual(response.status_code, 202)

    def test_server_rebuild_preserve_ephemeral_true(self):
        self._test_server_rebuild_preserve_ephemeral(True)

    def test_server_rebuild_preserve_ephemeral_false(self):
        self._test_server_rebuild_preserve_ephemeral(False)
