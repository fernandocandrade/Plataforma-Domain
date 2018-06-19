import logging
import sys

root = logging.getLogger("app")
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

def disable_log():
    root.setLevel(logging.CRITICAL)

def debug(msg):
    root.debug(msg)
def critical(msg):
    root.critical(msg, exc_info=msg)
def info(msg):
    root.info(msg)