#!/usr/bin/python 
# sqim clamav import program
# expects on stdin a file formatted with filename: match 
# will strip leading directory from the filename

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
            values=line.split(' ',1)
            if (len(values) < 2):
                break
            else:
                clamav=values[1].rstrip();
                malname=(values[0].split('/'))[1].split(':')
                #print values
                database.malware.update({'filename': malname[0]} ,
                                      {'$set': {'clamav': clamav}})
        
    connection.disconnect()
        

if __name__ == '__main__': 
    main(sys.argv[1:])
