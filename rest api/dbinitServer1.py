#!/usr/bin/python
# sqlalchemy section
import dbinit1 as dbcall
# python web framework
import cherrypy
# json example http://pymotw.com/2/json/
import json
import urllib
import string
import traceback

# find bad characters 
#http://club125.com/class/python101/lesson33.html
R_C = {}
for BadCharacters in string.digits + string.punctuation:
    R_C[BadCharacters] = None
    
class RestServerApi:
#http://tools.cherrypy.org/wiki/RestfulDispatch
    @cherrypy.expose
    def word(self, *args, **kwargs):
        if cherrypy.request.method == 'PUT':
		# if its a put method - send it to restput ( this file)
            return self.RestPut(*args, **kwargs)
			# send the arg and kwarg to rest put 
        else:
            raise cherrypy.HTTPError(501, 'Invalid request for URL.')
            
    @cherrypy.expose
    def words(self, *args, **kwargs):
        if cherrypy.request.method == 'GET':
            return self.RestGet(*args, **kwargs)
        else:
            print traceback.format_exc()
            raise cherrypy.HTTPError(501, 'Invalid request for URL.')
    
    
    
    def RestGet(self, *args, **kwargs):
        if len(args) == 0:
            WordsDbcall=dbcall.Words.getAll()
            return json.dumps(WordsDbcall)
        name = args[0]
        
        wordcount = dbcall.Words.getWordCount(name)
        if wordcount == None:
            wordcount = 0
        print "get request with no words to :/words/WORDNAME  gives the %s == %s" % (name, wordcount)
        return json.dumps( {name: wordcount} )
        

    def RestPut(self, *args, **kwargs):
        try:
            WORDNAME = urllib.unquote(args[0])
			#Replace %xx escapes by their single-character equivalent.
			#Example: unquote('/%7Econnolly/') yields '/~connolly/'.
			# test to see if its a word 
        except:
            raise cherrypy.HTTPError(501, 'Invalid URL, must specify WORDNAME')
        
        try:
#http://tools.cherrypy.org/wiki/JsonMimeType?format=txt  
#http://nullege.com/codes/show/src%40p%40e%40personis-0.933%40personis%40server%40server.py/430/cherrypy.request.body.read/python
            json_object = cherrypy.request.body.read()
	    json_string = json.loads(json_object)
        except:
            raise cherrypy.HTTPError(501, 'Invalid JSON body.')
# https://github.com/jbtule/keyczar-python2to3/blob/master/python/keyczar/keydata.py
        if type(json_string) != dict:
# check to see if its actually a key-pair
            raise cherrypy.HTTPError(501, 'Invalid JSON data structure. Expecting type hash.')
# from the curl input -d { word : xxxxx} - check the first part to see if it qualifies 
        if not 'word' in json_string:
            raise cherrypy.HTTPError(501, "Expecting hash key 'word' in JSON body, but wasn't found")
        word_split=json_string['word'].split() 			
        if not len(word_split) ==1:
            raise cherrypy.HTTPError(501, 'PUT requests must be one word in length')
        WORDNAME_Split = WORDNAME.split()        
        if not len(WORDNAME_Split) == 1:
            raise cherrypy.HTTPError(501, 'PUT requests must be one word in length')
        
        for _char in json_string['word']:
            if _char in restrictedCars:
                raise cherrypy.HTTPError(501, '%s is not a word. Contains invalid character.' % json_string['word'] )
            
        for _char in WORDNAME:
            if _char in restrictedCars:
                raise cherrypy.HTTPError(501, '%s restricted.' % WORDNAME )
            
        wordcount = dbcall.Words.putWord(json_string['word'])
        wordcount = dbcall.Words.putWord(WORDNAME)
        
        
    
def jsonErrPage(status, message, traceback, version):
    print traceback
    # json dumps the hash refrenced by the error key 
    return json.dumps( {'error': message} )

# don't forget double undescore 
if __name__ == '__main__':

# NOTE - for requirement of returning json on put error 
# Global config entries apply everywhere, and are stored in cherrypy.config. 
# This flat dict only holds global config data; 
# Global config is stored in the cherrypy.config dict, 
# and you therefore update it by calling cherrypy.config.update(conf). 
# The conf argument 
# cherrypy.config.update({'server.socket_host': '64.72.221.48','server.socket_port': 80,})
# def _error_page_501(status, message, traceback, version):
#        return message
#    cherrypy.config.update({'error_page.501': _error_page_501})
# http://client175.googlecode.com/svn-history/r119/trunk/server.py
# so when cherrypy.HTTPError returns 501 error - call jsonErrPage

    cherrypy.config.update( {'error_page.501': jsonErrPage} )

    dbcall.initSchema()
    cherrypy.quickstart( RestServerApi() )
    
