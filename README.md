# arangrecon
recon with subdomain listing, port scanning, dirsearch

```
                                      ____  ________________  _   __
  ____ __________ _____  ____ _      / __ \/ ____/ ____/ __ \/ | / /
 / __ `/ ___/ __ `/ __ \/ __ `/_____/ /_/ / __/ / /   / / / /  |/ /
/ /_/ / /  / /_/ / / / / /_/ /_____/ _, _/ /___/ /___/ /_/ / /|  /
\__,_/_/   \__,_/_/ /_/\__, /     /_/ |_/_____/\____/\____/_/ |_/
                      /____/

usage: arangrecon [-h] -d DOMAIN [-s] [-ds] [-o OUTPUT] [-oJ OUTPUT_JSON] [-q QUIET]

recon web service by input domain

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
  -s, --screenshot
  -ds, --dirsearch
  -o OUTPUT, --output OUTPUT
  -oJ OUTPUT_JSON, --output-json OUTPUT_JSON
  -q QUIET, --quiet QUIET
```

# Use Example

```
> python3 arangrecon.py -d arang.kr -oJ arang.kr_result.txt --screenshot --dirsearch
```
