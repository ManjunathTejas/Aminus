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
	     db.Keywords.update({"word":entity.name},{ "$set" : {"word":entity.name}}, upsert=True)
	     print('         name: {0}'.format(entity.name))
	     #print('         type: {0}'.format(entity.entity_type))
	     print('     metadata: {0}'.format(entity.metadata))
	     print('     salience: {0}'.format(entity.salience))
	resp = db.Keywords.find()
	arr = []
	for item in resp:
		arr.append(item['word'])
	file = open("words.txt","w")
	for item in arr:
		file.write(item)
		file.write("\n")
	file.close()
if __name__ == "__main__":
	main()
