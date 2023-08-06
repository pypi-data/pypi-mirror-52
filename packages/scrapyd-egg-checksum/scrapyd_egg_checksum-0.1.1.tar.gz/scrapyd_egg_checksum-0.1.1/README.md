# scrapyd-egg-checksum
Extension of scrapyd to get egg's md5 checksum for distributed scrapyd 

# Installation
```pip install scrapyd-egg-checksum```

# Configuration
Locate the ```scrapyd.conf``` file and adding line like 

```listversions_advanced.json = scrapyd_egg_checksum.webservice.ListVersions```

under service section, the json resource name depends on you, 

# Usage
```
curl http://127.0.0.1:6800/listversions_advanced.json?project=ABC
```

you will get like

```
{"node_name": "Christians-Another-MacBook-Pro.local", "status": "ok", "versions": [{"1_0_0": "793afec3676f9749d1616f48dd57fe07"}, {"1_0_1": "ccb6b8841e2b5443db4bff56924527fa"}]}
```


# Use case
This is for distributed scrapyd clusters, while in single server mode, this is useless.