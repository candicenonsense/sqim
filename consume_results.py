#!/usr/bin/python 
# for consuming results from sdhash
# accepts on stdin format filename|filename|score or pipes replaced w/tabs
# 2 arguments, first to name the result set and second to switch 
# the input filenames (not usually necessary) 

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
        
    tagname=sys.argv[1]
    switch=sys.argv[2]
    if connection is not None:
        for line in sys.stdin:
            values=line.split('\t',3)
            if (len(values) < 3):
                values=line.split('|',3)
                if (len(values) < 3):
                    break
            else:
                if ('/' in values[0]):
                    malname=(values[0].split('/'))[1]
                else:
                    malname=values[0]
                if ('/' in values[1]):
                    malname2=(values[1].split('/'))[1]
                else:
                    malname=values[1]
                score=values[2].rstrip()
                #print values
                #print malname, malname2, score
		if (switch=="Y"):
		    database.similar.insert({'name1': malname2, 'name2':malname, 'score':score,'tag':tagname})
                else:
		    database.similar.insert({'name1': malname, 'name2':malname2, 'score':score,'tag':tagname})
        
#    database.drop_collection('similar')
    connection.disconnect()

if __name__ == '__main__': 
    main(sys.argv[1:])
