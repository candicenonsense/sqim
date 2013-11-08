#!/usr/bin/python 

#
import sys
import pymongo

def main(args):

    mongodb_uri = 'mongodb://localhost:27017'
    db_name = 'malware'

    try:
        connection = pymongo.Connection(mongodb_uri)
        database = connection[db_name]
    except:
        print('Error: Unable to connect to database.')
        connection = None
        
    if connection is not None:

        party = database.malware.find({'md5': {'$in': sys.argv[1:] }})

        for foo in party:
             print foo
             #print foo['filename'], foo['md5'], foo['clamav']
	     similars1=database.similar.find({'name1':foo['filename']})
             for bar in similars1:
                 #print bar
                 ans=database.malware.find({'filename':bar['name2']},{'filename':1,'clamav':1,'md5':1})
		 for an in ans: 
                     print an['md5'],
		     if 'clamav' in an:
			  print an['clamav'],
                     print bar['score']
	     similars2=database.similar.find({'name2':foo['filename']})
             for bar in similars2:
                 #print bar
                 ans=database.malware.find({'filename':bar['name1']},{'filename':1,'clamav':1,'md5':1})
		 for an in ans: 
                     print an['md5'],
		     if 'clamav' in an:
			  print an['clamav'],
                     print bar['score']

if __name__ == '__main__': 
    main(sys.argv[1:])

