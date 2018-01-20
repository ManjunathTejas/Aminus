
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
	for entity in response.entities:
	     print('=' * 20)
	     print('         name: {0}'.format(entity.name))
	     #print('         type: {0}'.format(entity.entity_type))
	     print('     metadata: {0}'.format(entity.metadata))
	     print('     salience: {0}'.format(entity.salience))
if __name__ == "__main__":
	main()
