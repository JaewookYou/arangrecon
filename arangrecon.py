from arang import *
from pyfiglet import Figlet
import socket, os, traceback, time, sys, datetime, json
import xmltodict, argparse
from crawler import Crawler
from loguru import logger
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# you should set nmap path when your host is windows
nmappath = "nmap"

def verifyHttp(u):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
    try:
        r = requests.get(u, headers=headers, verify=False, timeout=15)
        return r
    except requests.exceptions.Timeout as e:
        printlog("info",f"[+] {u} is open but http unreachable")
        return False
    except requests.exceptions.SSLError:
        return False
    except requests.exceptions.ConnectionError:
        return False
    except KeyboardInterrupt:
        exit(1)
    except:
        printlog("error",u)
        printlog("error",traceback.format_exc())
        return False

def verifySock(d, p):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    try:        
        sock.connect((d, int(p)))
        sock.send(b"AAAA\n")
        r = sock.recv(4096)
        sock.close()
        return r    
    except (socket.timeout, TimeoutError):
        printlog("info",f"[+] {d}:{p} connected but timeout")
        return (f"[+] {d}:{p} connected but timeout").encode()
        return False
    except ConnectionResetError:
        printlog("info",f"[+] {d}:{p} connection aborted")
        return False
    except KeyboardInterrupt:
        exit(1)
        return False
    except:
        sock.close()
        printlog("error",traceback.format_exc())
        return False

def setResultDirs(domain):
    if not os.path.isdir(os.path.normpath("./results/")):
        os.mkdir(os.path.normpath("./results/"))
    nt = datetime.datetime.now()
    basedir = f"{domain}_{str(nt).replace(' ','_').replace(':','')[:-7]}"
    os.mkdir(os.path.normpath(f"./results/{basedir}/"))
    return basedir

def getsubdomains(domain, basedir):
    printlog("info",f"[+] get subdomains of {domain}")
    try:
        if os.name != 'nt':
            os.system(os.path.normpath(f"./subfinder/v2/subfinder -silent -o ./results/{basedir}/domains.txt -d {domain}"))
        elif os.name == 'nt':
            os.system(os.path.normpath(f"./subfinder/v2/subfinder.exe -silent -o ./results/{basedir}/domains.txt -d {domain}"))
    except:
        printlog("error","get subdomain error")
        return False
    
    time.sleep(0.5)
    
    return True


def parseArgs():
    parser = argparse.ArgumentParser(
        prog = 'arangrecon',
        description = 'recon web service by input domain',
    )
    parser.add_argument("-d", "--domain", help="target domain")
    parser.add_argument("-s", "--screenshot", action='store_true', help="take screenshot when opened port is assumed to HTTP(S)")
    parser.add_argument("-ds", "--dirsearch", action='store_true', help="do dirsearch when opened port is assumed to HTTP(S)")
    parser.add_argument("-o", "--output", help="save plain text result to given path")
    parser.add_argument("-oJ", "--output-json", help="save json type result to given path")
    parser.add_argument("-f", "--filter", help="only scan matched filter text")
    parser.add_argument("-p", "--passive", help="port scanning without subdomain listing, this argument get domain list file path")
    parser.add_argument("-fs", "--fullscan", help="full port scan(1-65535)")
    parser.add_argument("--ports", help="scan with given ports(file)")    
    parser.add_argument("-q", "--quiet", help="quiet mode")        
    args = parser.parse_args()
    
    if args.output != None and args.output_json != None:
        printlog("error", "[x] Please Select One Option with output(-o) or output_json(-oJ)")
    return args

def printAsciiArt(text):
    f = Figlet(font='slant')
    print(f.renderText(text))

def printlog(logtype, text):
    global args
    if not args.quiet:
        if logtype == "info":
            logger.info(text)
        elif logtype == "success":
            logger.success(text)
        elif logtype == "warning":
            logger.warning(text)
        elif logtype == "error":
            logger.error(text)
        else:
            logger.info(text)

printAsciiArt("arang-RECON")
args = parseArgs()

if args.domain == None and args.passive == None:
    printlog("error", "[x] you didn't put any domain or domains")
    exit(1)

basedir = setResultDirs(args.domain)
if not args.passive:
    if getsubdomains(args.domain, basedir):
        with open(os.path.normpath(f"./results/{basedir}/domains.txt"), "r") as f:
            domains = f.read().split("\n")
            if "" in domains:
                domains.remove("")
elif args.passive != None:
    with open(os.path.normpath(args.passive),"r") as f:
        domains = f.read().split("\n")
        if "" in domains:
            domains.remove("")
else:
    printlog("error",f"[x] subdomain finding failed")
    exit(1)

if args.ports != None:
    with open(os.path.normpath(args.ports),"r") as f:
        givenports = f.read().split("\n")
        if "" in domains:
            domains.remove("")


if args.screenshot:    
    os.mkdir(os.path.normpath(f"./results/{basedir}/screenshots/"))
    crawler = Crawler()

if args.dirsearch:
    os.mkdir(os.path.normpath(f"./results/{basedir}/dirsearch/"))

results = {}
driver = None
cnt = 0
printlog("info",f"[+] do port scanning, if you should input sudo password, plz input sudo password")
for url in domains:
    if args.filter != None:
        if args.filter not in url:
            printlog("info",f"[+] {args.filter} not in {url}.. pass")
            continue
    try:
        result = ""
        if args.passive:
            ip = url
        else:
            ip = socket.gethostbyname(url)
        printlog("info",f"[+] {url} scanning start")
        fname = os.path.normpath(f"./results/{basedir}/{url.replace('/','_')}_result.xml")
        if os.name != 'nt':
            if args.fullscan != None:
                os.system(f"sudo nmap -sS -Pn -p 1-65535 -v0 {ip} -oX {fname}")
            else:
                if givenports:
                    portOption = ",".join(givenports)
                    print(f"sudo nmap -sS -v0 {ip} -oX {fname} -Pn -p {portOption}")
                    os.system(f"sudo nmap -sS -v0 {ip} -oX {fname} -Pn -p {portOption}")
                else:
                    os.system(f"sudo nmap -sS -v0 {ip} -oX {fname}")
                
        elif os.name == 'nt':            
            if args.fullscan != None:
                os.system(f"{nmappath} -sS -Pn -p 1-65535 -v0 {ip} -oX {fname}")
            else:
                if givenports:
                    portOption = ",".join(givenports)
                    os.system(f"nmap -sS -v0 {ip} -oX {fname} -Pn -p {portOption}")
                else:
                    os.system(f"nmap -sS -v0 {ip} -oX {fname}")
        time.sleep(0.5)
        with open(fname,"r") as f:
            xmlfile = f.read()
        jsonfile = xmltodict.parse(xmlfile)
        
        hostname = ""
        
        if "host" not in jsonfile["nmaprun"]:
            printlog("info",f"[x] {url} has no host")
            continue

        if jsonfile["nmaprun"]["host"]["hostnames"] != None:
            hostname = jsonfile["nmaprun"]["host"]["hostnames"]["hostname"]["@name"]
        
        if "port" not in jsonfile["nmaprun"]["host"]["ports"]:
            printlog("info",f"[x] {url} scanning result has no ports")
            continue
        
        ports = jsonfile["nmaprun"]["host"]["ports"]["port"]
        
        if type(ports) == dict:
            ports = [ports]
        
        for port in ports:
            if port["state"]["@state"] == "open":
                t = f"\n[+] {url}({ip}, {hostname}) - port {port['@portid']}({port['service']['@name']}) open\n"
                printlog("success",t)
                result += t

                if url not in results:
                    results[url] = {}
                
                if "port" not in results[url]:
                    results[url]["port"] = {}
                
                results[url]["port"][port['@portid']] = {}
                results[url]["port"][port['@portid']]["open"] = True
                results[url]["port"][port['@portid']]["service_name"] = port['service']['@name']
                results[url]["port"][port['@portid']]["ip"] = ip

                u = f"http://{url}:{port['@portid']}/"
                r = verifyHttp(u)
                if r:
                    if r.status_code == 200:
                        t = f"[+] {u} http requests success - (length : {len(r.content)})\n\n"
                        result += t
                        printlog("success",t)

                        results[url]["port"][port['@portid']]["http"] = True

                        if args.screenshot:
                            printlog("info", f"[+] take screenshot of {u}")                            
                            driver = crawler.req(u)
                            driver.save_screenshot(f'./results/{basedir}/screenshots/{url}.png')                            
                        
                        if args.dirsearch:
                            printlog("info", f"[+] do dirsearch of {u}")
                            os.system(f'python3 ./dirsearch/dirsearch.py -u "{u}" -e swp,bak,tar,war,zip,txt,html,js -o ./results/{basedir}/dirsearch/{url}.txt --format plain')
                    else:
                        t = f"[+] {u} http reuqests success but not 200 (length : {r.status_code})\n\n"
                        result += t
                        printlog("success",t)
                
                u = f"https://{url}:{port['@portid']}/"
                r = verifyHttp(u)
                if r:
                    if r.status_code == 200:
                        t = f"[+] {u} https requests success - (length : {len(r.content)})\n\n"
                        result += t
                        printlog("success",t)

                        results[url]["port"][port['@portid']]["https"] = True

                        if args.screenshot:
                            printlog("info", f"[+] take screenshot of {u}")
                            driver = crawler.req(u)
                            driver.save_screenshot(f'./results/{basedir}/screenshots/{url}.png')
                            
                    else:
                        t = f"[+] {u} https reuqests success but not 200 (length : {r.status_code})\n\n"
                        result += t
                        printlog("success",t)
                
                r = verifySock(ip, port['@portid'])
                if r:
                    if len(r) > 30:
                        r = r[:30]+b" ... "
                    t = f"[+] {u}({ip}) socket recv data - {r} (length : {len(r)})\n\n"
                    result += t
                    printlog("success",t)
                    
                    results[url]["port"][port['@portid']]["len"] = len(r)
                    results[url]["port"][port['@portid']]["response"] = str(r)

        os.remove(fname)

        with open(os.path.normpath(f"./results/{basedir}/scan_result.txt"), "a+") as f:
            f.write(result+"\n----------------------------------\n")
    except KeyboardInterrupt:
        exit(1)
    except Exception as e:        
        if "[Errno 8]" in str(e):
            printlog("info",f"[x] {url} doesn't have dns")
            continue
        
        printlog("error",traceback.format_exc())

if driver:
    driver.quit()

if args.output != None or args.output_json != None:
    printlog("info","[+] write output to file")
    if args.output_json != None:
        output_path = args.output_json
        output = json.dumps(results, sort_keys=True, indent=4)
    else:
        output_path = args.output
        output = result

    with open(output_path, "w+") as f:
        f.write(output)
