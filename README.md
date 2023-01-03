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
                        target domain
  -s, --screenshot      take screenshot when opened port is assumed to HTTP(S)
  -ds, --dirsearch      do dirsearch when opened port is assumed to HTTP(S)
  -o OUTPUT, --output OUTPUT
                        save plain text result to given path
  -oJ OUTPUT_JSON, --output-json OUTPUT_JSON
                        save json type result to given path
  -q QUIET, --quiet QUIET
                        quiet mode
```

# Use Example

```
> python3 arangrecon.py -d arang.kr -oJ arang.kr_result.txt --screenshot --dirsearch
```
