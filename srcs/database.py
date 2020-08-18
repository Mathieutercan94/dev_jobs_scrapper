import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv('MONGO_URL')

client = pymongo.MongoClient(MONGO_URL)


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
