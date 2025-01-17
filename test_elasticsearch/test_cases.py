#  Licensed to Elasticsearch B.V. under one or more contributor
#  license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright
#  ownership. Elasticsearch B.V. licenses this file to you under
#  the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

from collections import defaultdict

from elasticsearch import Elasticsearch


class DummyTransport(object):
    def __init__(self, hosts, responses=None, **_):
        self.hosts = hosts
        self.responses = responses
        self.call_count = 0
        self.calls = defaultdict(list)

    def perform_request(self, method, url, params=None, headers=None, body=None):
        resp = 200, {}
        if self.responses:
            resp = self.responses[self.call_count]
        self.call_count += 1
        self.calls[(method, url)].append((params, headers, body))
        return resp


class DummyTransportTestCase:
    def setup_method(self, _):
        self.client = Elasticsearch(transport_class=DummyTransport)

    def assert_call_count_equals(self, count):
        assert count == self.client.transport.call_count

    def assert_url_called(self, method, url, count=1):
        assert (method, url) in self.client.transport.calls
        calls = self.client.transport.calls[(method, url)]
        assert count == len(calls)
        return calls
