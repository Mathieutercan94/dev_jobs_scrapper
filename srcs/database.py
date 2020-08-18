import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASS = os.getenv('MONGO_PASS')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')

client = pymongo.MongoClient("mongodb+srv://{}:{}@stationfjobsscrapper.3wr5d.mongodb.net/jobs_database?retryWrites=true&w=majority".format(MONGO_USER, MONGO_PASS))


def is_url_in_database(url):
	"""
	Return True if the given URL is already in our MongoDB database.
	url: String
	"""

	conds = {
		'url': url
	}

	o = client.jobs_database.jobs_collection.find_one(conds)

	return o is not None


def add_url_in_database(url):
	"""
	Add an URL into our MongoDB database.
	url: String
	"""

	doc = {
		'url': url
	}

	client.jobs_database.jobs_collection.insert_one(doc)
