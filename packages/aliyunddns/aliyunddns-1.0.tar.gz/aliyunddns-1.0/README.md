# Aliyun DDNS
A dynamic DNS client for Aliyun written in pure Python.

## Install
Download and install the `aliyunddns` package for Python.
```
pip install aliyunddns
```
## Usage:
There are two ways to pass arguments to the program:
1. Passing a config file path with `-c` argument.
2. Specify information using the command line arguments.

Note: when passing a config file, all the other arguments will be ignored.

Here are the full arguments list:
```cmd
usage: ddns.py [-h] [-c CONFIG] [--access-key ACCESS_KEY]
               [--secret-key SECRET_KEY] [--domain DOMAIN]
               [--host-record HOST_RECORD] [--line LINE] [--ttl TTL]
               [--log-file LOG_FILE]

Aliyun DDNS Client

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG             config file path (ignore other arguments)
  --access-key ACCESS_KEY
                        access Key Id
  --secret-key SECRET_KEY
                        secret Key
  --domain DOMAIN       domain name
  --host-record HOST_RECORD
                        host record
  --line LINE           line <default|telecom|unicom|mobile|oversea|edu|drpeng
                        |btvn>
  --ttl TTL             TTL
  --log-file LOG_FILE   log file path
```
## Config
The config file format is JSON. Create a config file with extension `.json` and convert the dash in command line arguments to underline.

For examples:
```json
{
  "access_key": "abc",
  "secret_key": "abc",
  "domain": "example.com",
  "host_record": "@",
  "line": "default",
  "ttl": 600,
  "log_file": "/var/log/ddns/ddns.log"
}
```

## Examples
1. Specify a config file.
```cmd
aliyunddns -c config.json
```
2. Using command line arguments.
```cmd
aliyunddns --access-key=abc --secret-key=abc --domain=example.com --log-file=/var/log/ddns/ddns.log
```
