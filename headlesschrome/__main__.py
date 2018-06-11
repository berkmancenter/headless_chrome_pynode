from .__init__ import Client
import argparse, logging

logging.basicConfig(level=logging.WARN)
parser = argparse.ArgumentParser(description='Save a URL as a HAR file and screenshot')
parser.add_argument('url', help='URL to download')
args = parser.parse_args()
print(Client().capture(args.url))
