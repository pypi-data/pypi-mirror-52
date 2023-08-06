pycloudflare
============

Provides a class and methods to interact with the CloudFlare Workers KV service.

In the future it will support more API endpoints with CloudFlare.

This project is not affiliated with CloudFlare in any way and CloudFlare and associated copyrights belong to CloudFlare.

Usage
--

    from pycloudflare import CloudFlare
    
    # I would recommend using environmental variables or 
    # some other method that does not hard-code your secrets.
    auth_email = "YOUR_CLOUDFLARE_AUTH_EMAIL"
    auth_key = "YOUR_CLOUDFLARE_AUTH_KEY"
    accound_id = "YOUR_CLOUDFLARE_ACCOUNT_ID"
    
    cf = CloudFlare(auth_email, auth_key)
    
    # Get all Namespaces
    namespaces = cf.storage.get_namespaces(account_id)
    ## cf.storage can also be cf.kv.get_namespaces(account_id)
    
    # Create a new Namespace
    new_namespace = cf.storage.create_namespace(accound_id, "test")
    
    # Write Key-Value
    cf.storage.write_key(account_id, new_namespace.id, "hello", "world")
    
    # Get Key-Value
    print(cf.storage.get_key(account_id, new_namespace.id, "hello"))
    
    # Iterate over keys in Namespace
    keys = cf.storage.namespace_keys(account_id, new_namespace.id)
    print(keys)
    for key in keys:
        print(cf.storage.get_key(account_id, new_namespace.id, key))
        
    # Delete a key
    cf.storage.delete_key(account_id, new_namespace.id, "hello")
    
    # Renaming a Namespace
    cf.storage.rename_namespace(account_id, new_namespace.id, "new_test"))
    
    # Iterating over Namespaces
    namespaces = cf.storage.get_namespaces(account_id)
    for namespace in namespaces:
        print(namespace)
        
    # Bulk Writes
    cf.storage.bulk_write(account_id, new_namespace.id,
                          [{"key": "world", "value": "hello"},
                           {"key": "jello", "value": "mold"}])
    
    # Bulk Deletes
    cf.storage.bulk_delete(account_id, new_namespace.id, ["jello", "world"])
    
    # Delete a Namespace
    cf.storage.delete_namespace(account_id, new_namespace.id)
    


Contributing
---

* Keep it simple. 

* Don't make breaking changes, like ever.

* Submit a pull request.

Issues
---

This will be maintained for as long as I am using CloudFlare, don't hesitate to open an issue.

Roadmap
---

* Add support for registering account IDs to a name. (Quality of Life)
* Add support for cache API.
* Add support for routes API.
* Add support for DNS API.

Suggestions are welcome.

License
---

Copyright (C) 2019 by Bill Schumacher

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.