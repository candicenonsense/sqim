#!/usr/bin/python 
# filename/md5 load - run before any other load scripts
# expects format md5 filename on stdin.

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
        for line in sys.stdin:
            values=line.split();
            md5=values[0]
            malname=values[1].split('/');
            #print "md5 ",md5," name ", malname[1]
            database.malware.insert({'filename': malname[1] , 'md5':md5} )
            #print ".",

        #database.drop_collection('malware')
        connection.disconnect()
        
    #print
if __name__ == '__main__': 
    main(sys.argv[1:])
