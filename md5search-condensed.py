#!/usr/bin/python 
# search for 1 or more md5s given on command line
# returns json containing antivirus match/sdhash score and 
# counts of the returns

import sys
import pymongo
import json
from collections import Counter

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
        
    if connection is not None:

        party = database.malware.find({'md5': {'$in': sys.argv[1:] }})
	hugeobject=[]
        for foo in party:
             reslist=[]
	     stringlist=[]
             #print "Query " foo['filename'], foo['md5'], foo['clamav']
	     similars1=database.similar.find({'name1':foo['filename']})
             for bar in similars1:
                 ans=database.malware.find({'filename':bar['name2']},{'filename':1,'clamav':1,'md5':1})
		 for an in ans: 
		     if 'clamav' in an:
			 #print an['md5'], an['clamav'], bar['score']
                         result=dict(name=an['clamav'],size=bar['score'],md5=an['md5'])
                         res2="av: "+an['clamav']+" score: "+bar['score']
			 reslist.append(result)
			 stringlist.append(res2)
	     similars2=database.similar.find({'name2':foo['filename']})
             for bar in similars2:
                 ans=database.malware.find({'filename':bar['name1']},{'filename':1,'clamav':1,'md5':1})
		 for an in ans: 
		     if 'clamav' in an:
			 #print an['md5'], an['clamav'], bar['score']
                         result=dict(name=an['clamav'],size=bar['score'],md5=an['md5'])
                         res2="av: "+an['clamav']+" score: "+bar['score']
			 reslist.append(result)
			 stringlist.append(res2)
	     counted=Counter(stringlist)
	     #print c.items()
	     endlist=[]
	     for c in counted.items():
                 #print dict(name=c[0],size=c[1])
                 endlist.append(dict(name=c[0],size=c[1]))
             hugeobject.append(dict(name=foo['filename'],children=endlist,size=len(endlist),md5=foo['md5']))
        fin=dict(name="malware",children=hugeobject) 
        print json.dumps(fin) 

if __name__ == '__main__': 
    main(sys.argv[1:])

