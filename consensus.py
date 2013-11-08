#!/usr/bin/python 

# pymongo_example_simple.py
# 
# A sample python script covering connection to a MongoDB database given a
# fully-qualified URI. There are a few alternate methods, but we prefer the URI
# connection model because developers can use the same code to handle various
# database configuration possibilities (single, master/slave, replica sets).
#
# Author::  MongoLab

# First, require the pymongo MongoDB driver.
#
import sys
import pymongo
import json
from bson.code import Code

def main(args):

    # If your database server is running in auth mode, you will need user and
    # database info. Ex:
    #    mongodb_uri = 'mongodb://username:password@localhost:27017/dbname'
    #
    mongodb_uri = 'mongodb://localhost:27017'
    db_name = 'malware'

    # pymongo.Connection creates a connection directly from the URI, performing
    # authentication using the provided user components if necessary.
    #
    try:
        connection = pymongo.Connection(mongodb_uri)
        database = connection[db_name]
    except:
        print('Error: Unable to connect to database.')
        connection = None
    tagname=sys.argv[1] 
    scorethr=sys.argv[2] 
    # What follows is insert, update, and selection code that can vary widely
    # depending on coding style.
    #
    reducer = Code(""" function(obj, prev){ prev.count++;} """)
    if connection is not None:

        stuff =database.similar.count()
	#print stuff
        malgroup=database.similar.group(key={'name1':1},condition={'tag':tagname,'score': {'$gte':scorethr}},initial={'count':0},reduce=reducer)

        hugeobject=[]
        #malgroup=database.malware.find({'name1':)
        for bar in malgroup:
            ours=database.similar.find({'name1': bar['name1'],'score':{'$gte':scorethr}})
            thesenames=[]
            for some in ours:
		#print some['name2']
                thesenames.append(some['name2'])
            avres=database.malware.group(key={'clamav': 1},condition={'filename': { '$in': thesenames }},initial={"count":0},reduce=reducer)
            reslist=[]
            for more in avres:
                if (more['clamav']=='OK'):
                    continue
                foo=dict(name=more['clamav'],size=more['count'])
                reslist.append(foo)
            newlist=sorted(reslist,key=lambda k: k['size'])
            newlist.reverse()
            allist=dict(name=bar['name1'],children=newlist,size=len(newlist))
            hugeobject.append(allist)
            #info=database.malware.find({'filename':bar['name1']})
            #for md5s in info:
            #    allist=dict(name=md5s['md5'],children=newlist,size=len(newlist))
            #    hugeobject.append(allist)
            newhuge=sorted(hugeobject,key=lambda k: k['size'])
            newhuge.reverse()
            
        final=dict(name="malware",children=newhuge) 
        print json.dumps(final)

if __name__ == '__main__': 
    main(sys.argv[1:])

