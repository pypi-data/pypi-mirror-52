# Neptune Resolver Rest
This module is made as a caching middleware for Neptune DNS server
## Installation
```pip3 install neptune_cache_redis```
## Connect to server
In config.py edit CACHE variable. Add ```'neptune_cache_redis'```  
It will look like this  
```CACHE = 'neptune_cache_redis'```  
Then you need to set settings for this cacher. Those settings are set by creating variable   in config.py with upper module name like this  
```NEPTUNE_CACHE_REDIS = {'host':'localhost', 'database': 1}```