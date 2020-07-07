# f5_scanner
F5 mass scanner and  CVE-2020-5902 checker

# This tool is mass scanner with 30 threads hardcoded use with caution

## How to setup
```
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install -r requirements.txt
```
## How to run

### Single IP

python3 f5_scanner.py --ip 192.168.1.1

### CIDR

python3 f5_scanner.py --cidr 192.168.0.0/24

### File
the file should be 1 by line set of single ip address eg :

```
192.168.0.1
192.168.0.2
192.168.0.3
```

python3 f5_scanner.py --file file_with_ips.txt


