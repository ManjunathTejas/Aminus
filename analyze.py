import pymongo
from pymongo import MongoClient
from pprint import pprint
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def main():
	# Instantiates a client
	client = language.LanguageServiceClient()

	# The text to analyze
	file = open("transcribed.txt","rw+")
	text = file.readline()
	document = language.types.Document(
	    content=text,
	     type=language.enums.Document.Type.PLAIN_TEXT,
	)

	# Detects the sentiment of the text
	response = client.analyze_entities(
	     document=document,
	     encoding_type='UTF32',
	 )
	client = MongoClient("localhost",27017)
	db = client.admin
	for entity in response.entities:
	     print('=' * 20)
	     print entity.name
	     if db.Keywords.find_one({"word":entity.name}) is None:
		db.Keywords.insert({"word":entity.name}, {"count":5})
	     else:
	        db.Keywords.update({"word":entity.name}, { "$inc": {"count": 1}})
             print db.Keywords.find_one({"word":entity.name})
	     print('         name: {0}'.format(entity.name))
	     #print('         type: {0}'.format(entity.entity_type))
	     print('     metadata: {0}'.format(entity.metadata))
	     print('     salience: {0}'.format(entity.salience))
        resp = db.Keywords.find().sort("count",pymongo.DESCENDING)
	arr = []
	i = 0
	for item in resp:
		if i == 5:
			break
		arr.append(item['word'])
		i += 1
	file = open("data.txt","w")
	i = 1
	for item in arr:
		file.write('<p id="p')
		file.write(str(i))
		file.write('">')
		file.write(item)
		file.write('</p>')
		file.write("\n")
		i += 1
	file.close()
if __name__ == "__main__":
	main()
