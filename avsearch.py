#!/usr/bin/python 
# simple filname to md5 lookup 
# accepts one or more filenames 
# returns json-structured information

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

        party = database.malware.find({'clamav': {'$regex': sys.argv[1] }})

        for foo in party:
             print foo


if __name__ == '__main__': 
    main(sys.argv[1:])

