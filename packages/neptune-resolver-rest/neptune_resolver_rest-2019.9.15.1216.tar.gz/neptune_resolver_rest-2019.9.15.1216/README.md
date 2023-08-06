# Neptune Resolver Rest
This module is made as a resolving middleware for Neptune DNS server
## Installation
```pip3 install neptune_resolver_rest```
## Connect to server
In config.py edit RESOLVERS variable. Add ```'neptune_resolver_rest'```
It will look like this
```RESOLVERS = ['neptune_resolver_rest']```
Then you need to set settings for this resolver. Those settings are set by creating variable in config.py with upper module name like
```NEPTUNE_RESOLVER_REST = {'base_url':'https://example.com'}```