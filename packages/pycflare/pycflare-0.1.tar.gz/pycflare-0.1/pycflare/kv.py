# -*- coding: utf-8 -*-
# Copyright (C) 2019 by Bill Schumacher
#
# Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby
# granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

import json


class Namespace(object):
    def __init__(self, id=None, title=None, *args, **kwargs):
        self.id = id
        self.title = title

    def __repr__(self):
        return "Namespace(id='{id}', title='{title}')".format(id=self.id, title=self.title)


class Key(object):
    def __init__(self, name, value, *args, **kwargs):
        self.name = name
        self.value = value

    def __repr__(self):
        return "Key(name='{name}', value='{value}')".format(name=self.name, value=self.value)


class Storage(object):
    """
        CloudFlare Workers Key-Value storage module.

        Provides methods to interact with the CloudFlare Workers KV API.
    """
    create_namespace_url = "{base}/accounts/{account_id}/storage/kv/namespaces"
    get_namespaces_url = "{base}/accounts/{account_id}/storage/kv/namespaces?page={page}&per_page={per_page}"
    delete_namespace_url = "{base}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}"
    namespace_keys_url = "{base}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/keys?limit={limit}"
    rename_namespace_url = "{base}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}"
    get_key_url = "{base}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key_name}"
    write_key_url = "{base}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key_name}"
    bulk_write_url = "{base}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/bulk"
    bulk_delete_url = "{base}/accounts/{account_id}/storage/kv/namespaces/{namespace_id}/bulk"
    query_request_analytics_url = "{base}/accounts/{account_id}/storage/analytics?limit={limit}"

    def __init__(self, cf):
        """
        Initializes the CloudFlare Workers Key-Value storage module.

        This class should not need to be initialized manually.

        :param cf: The CloudFlare instance, stores commonly used methods and data.
        """
        self.cf = cf

    def create_namespace(self, account_id, title):
        """
        Creates a new Namespace.

        :param account_id: Your CloudFlare account ID.
        :param title: The title or name of your new Namespace.
        :return: Returns a Namespace class or None on failure.
        """
        request_url = self.create_namespace_url.format(base=self.cf.api_base, account_id=account_id)
        headers = self.cf.get_headers()
        response = self.cf.try_post_request(request_url, headers=headers, data=json.dumps(dict(title=title)))
        result = response.get("result")
        if result is not None:
            return Namespace(**result)
        return None

    def get_namespaces(self, account_id, page=1, per_page=20):
        """
        Returns a paginated list of Namespaces for the account.

        :param account_id: Your CloudFlare account ID.
        :param page: The page you want to view.
        :param per_page: The number of results per page.
        :return: Returns a list of Namespace objects or None on failure.
        """
        request_url = self.get_namespaces_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            page=page,
            per_page=per_page
        )
        headers = self.cf.get_headers()
        response = self.cf.try_get_request(request_url, headers=headers)
        results = response.get("result")
        if results is not None:
            if type(results) == list:
                namespaces = []
                for result in results:
                    namespaces.append(Namespace(**result))
                return namespaces
            return None
        return None

    def delete_namespace(self, account_id, namespace_id):
        """
        Deletes a Namespace from the account.

        :param account_id: Your CloudFlare account ID.
        :param namespace_id: The Namespace UUID.
        :return: A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """
        request_url = self.delete_namespace_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            namespace_id=namespace_id
        )
        headers = self.cf.get_headers()
        return self.cf.try_delete_request(request_url, headers=headers)

    def rename_namespace(self, account_id, namespace_id, title):
        """
        Rename's a Namespace for the account.

        :param account_id: Your CloudFlare account ID.
        :param namespace_id: The Namespace UUID.
        :param title: The new title.
        :return: Returns the Namespace or None on failure.
        """
        request_url = self.rename_namespace_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            namespace_id=namespace_id
        )
        headers = self.cf.get_headers()
        return self.cf.try_put_request(request_url, headers=headers, data=json.dumps(dict(title=title)))

    def namespace_keys(self, account_id, namespace_id, limit=1000, cursor=None, prefix=None):
        """
        Gets a list of Keys in the Namespace for the account.

        :param account_id: Your CloudFlare account ID.
        :param namespace_id: The Namespace UUID.
        :param limit: The maximum number of results.
        :param cursor: The key name to start from.
        :param prefix: The prefix to filter by.
        :return: A list of strings or None on failure.
        """
        request_url = self.namespace_keys_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            namespace_id=namespace_id,
            limit=limit
        )
        self.cf.apply_filters(request_url, cursor=cursor, prefix=prefix)
        response = self.cf.try_get_request(request_url, headers=self.cf.get_headers())
        results = response.get("result")
        if results is not None:
            if type(results) == list:
                keys = []
                for result in results:
                    keys.append(result.get("name"))
                return keys
            return None
        return None

    def get_key(self, account_id, namespace_id, key_name):
        """
        Get a key-value pair from the Namespace for the account.

        :param account_id: Your CloudFlare account ID.
        :param namespace_id: The Namespace UUID.
        :param key_name: The name of the Key in the Namespace.
        :return: A Key object.
        """
        request_url = self.get_key_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            namespace_id=namespace_id,
            key_name=key_name)
        headers = self.cf.get_headers()
        response = self.cf.try_get_request(request_url, headers=headers)
        result = response.get("result")
        if result is not None:
            try:
                return Key(name=key_name, value=json.loads(result))
            except json.decoder.JSONDecodeError:
                return Key(name=key_name, value=result)
        return None

    def write_key(self, account_id, namespace_id, key_name, data, expiration=None, expiration_ttl=None):
        """
        Creates or updates a Key-Value pair in the Namespace for the account.

        :param account_id: Your CloudFlare account ID.
        :param namespace_id: The Namespace UUID.
        :param key_name: The name of the Key in the Namespace.
        :param data: The value to write.
        :param expiration: The expiration in time since EPOCH in seconds.
        :param expiration_ttl: The expiration in seconds.
        :return:A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """
        request_url = self.write_key_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            namespace_id=namespace_id,
            key_name=key_name)
        request_url = self.cf.apply_filters(request_url, expiration=expiration, expiration_ttl=expiration_ttl)
        headers = self.cf.get_headers()
        headers["Content-Type"] = "text/plain"
        return self.cf.try_put_request(request_url, headers=headers, data=data)

    def bulk_write(self, account_id, namespace_id, data):
        """
        Write multiple Key-Value pairs to the Namespace for the account.
        :param account_id: Your CloudFlare account ID.
        :param namespace_id: The Namespace UUID.
        :param data: A list Key names, values and options to write.
        Example: [{"key": "hello", "value": "world"}, ...]
        :return:
        """
        request_url = self.bulk_write_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            namespace_id=namespace_id)
        headers = self.cf.get_headers()
        try:
            return self.cf.try_put_request(request_url, headers=headers, data=json.dumps(data))
        except json.decoder.JSONDecodeError:
            return None

    def delete_key(self, account_id, namespace_id, key_name):
        """
        Delete a Key-Value pair from the Namespace for the account.

        :param account_id: Your CloudFlare account ID.
        :param namespace_id: The Namespace UUID.
        :param key_name:
        :return:A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """
        request_url = self.get_key_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            namespace_id=namespace_id,
            key_name=key_name)
        headers = self.cf.get_headers()
        return self.cf.try_delete_request(request_url, headers=headers)

    def bulk_delete(self, account_id, namespace_id, keys):
        """
        Delete multiple Key-Value pairs from the Namespace for the account.

        :param account_id: Your CloudFlare account ID.
        :param namespace_id: The Namespace UUID.
        :param keys: The keys to delete, example ["Hello", "World", ...]
        :return: A json response output.
        Success Example:
        {'result': None, 'success': True, 'errors': [], 'messages': []}
        """
        request_url = self.bulk_delete_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            namespace_id=namespace_id)
        headers = self.cf.get_headers()
        try:
            return self.cf.try_delete_request(request_url, headers=headers, data=json.dumps(keys))
        except json.decoder.JSONDecodeError:
            return None

    def query_request_analytics(self, account_id, limit=10000, since=None, until=None, metrics=None, dimensions=None,
                                sort=None, filters=None):
        """

        :param account_id:
        :param limit:
        :param since:
        :param until:
        :param metrics:
        :param dimensions:
        :param sort:
        :param filters:
        :return:
        """
        request_url = self.query_request_analytics_url.format(
            base=self.cf.api_base,
            account_id=account_id,
            limit=limit
        )
        request_url = self.cf.apply_filters(request_url, since=since, until=until, metrics=metrics,
                                            dimensions=dimensions, sort=sort, filters=filters)
        return self.cf.try_get_request(request_url, headers=self.cf.get_headers())

    def query_stored_data_analytics(self, account_id, limit=10000, since=None, until=None, metrics=None,
                                    dimensions=None, sort=None, filters=None):
        """

        :param account_id:
        :param limit:
        :param since:
        :param until:
        :param metrics:
        :param dimensions:
        :param sort:
        :param filters:
        :return:
        """
        request_url = "{base}/accounts/{account_id}/storage/analytics/stored?limit={limit}".format(
            base=self.cf.api_base,
            account_id=account_id,
            limit=limit
        )
        request_url = self.cf.apply_filters(request_url, since=since, until=until, metrics=metrics,
                                            dimensions=dimensions, sort=sort, filters=filters)
        return self.cf.try_get_request(request_url, headers=self.cf.get_headers())
