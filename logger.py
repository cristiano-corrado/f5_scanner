import codecs
import json
import logging
import logging.config
import sys
import os

"""
This file will help consolidating logging mechanism throughout the project
"""

abspath=os.path.abspath(".")
# Initiate config from config file
confdir = "conf"
logdir = "logs"
sect = abspath.split("/")

for i in range(len(sect)):
    if not any( n == confdir for n in  os.listdir("/".join(sect))):
        sect.pop(-1)
    else:
        abspath="/".join(sect)
        break

with codecs.open(abspath+"/conf/logging.json", "r", encoding="utf-8") as fd:
    config = json.load(fd)


# Set up proper logging. This one disables the previously configured loggers.
logging.config.dictConfig(config)