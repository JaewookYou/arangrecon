# arangrecon
recon with subdomain listing, port scanning, dirsearch
```
                                      ____  ________________  _   __
  ____ __________ _____  ____ _      / __ \/ ____/ ____/ __ \/ | / /
 / __ `/ ___/ __ `/ __ \/ __ `/_____/ /_/ / __/ / /   / / / /  |/ / 
/ /_/ / /  / /_/ / / / / /_/ /_____/ _, _/ /___/ /___/ /_/ / /|  /  
\__,_/_/   \__,_/_/ /_/\__, /     /_/ |_/_____/\____/\____/_/ |_/   
                      /____/                                        

usage: arangrecon [-h] [-d DOMAIN] [-s] [-ds] [-o OUTPUT] [-oJ OUTPUT_JSON] [-f FILTER] [-p PASSIVE] [-fs FULLSCAN] [--ports PORTS] [-q QUIET]

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
  -f FILTER, --filter FILTER
                        only scan matched filter text
  -p PASSIVE, --passive PASSIVE
                        port scanning without subdomain listing, this argument get domain list file path
  -fs FULLSCAN, --fullscan FULLSCAN
                        full port scan(1-65535)
  --ports PORTS         scan with given ports(file)
  -q QUIET, --quiet QUIET
                        quiet mode
```

# how to install

### when you clone git repository, you should give `--recurse-submodules` option
```
> git clone --recurse-submodules https://github.com/jaewookyou/arangrecon
```

### build subfinder(for linux/mac)
```
> cd subfinder/v2
> make
```
### build subfinder(for windows)
 * you should download `go` for windows([install here](https://go.dev/dl/))
 * install subfinder by `go install`
```
> go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```
 * move subfinder binary(usually at `C:\Users\%USERNAME%\go\bin\subfinder.exe`) to `.\arangrecon\subfinder\v2\`

### install python libraries(linux / mac)
```
> python3 -m pip install -r requirements.txt
```

### install python libraries(win)
```
> python3 -m pip install -r requirements_win.txt
```

### [ONLY FOR WINDOWS] setting `nmappath` variable to use nmap
```python
...

# you should set nmap path when your host is windows
nmappath = "%your nmap binary path at here%"

...
```

# Use Example

```
> python3 arangrecon.py -d arang.kr -oJ arang.kr_result.txt --screenshot --dirsearch -fs
```
- if use this options,
1. subdomain find by "arang.kr"
2. json output to "arang.kr_result.txt"
3. nmap scan(with fullscan(-fs)) subdomains which is identified by subfinder
4. take screenshot when exposure port is HTTP(S) service
5. do dirsearch when exposure port is HTTP(S) service
