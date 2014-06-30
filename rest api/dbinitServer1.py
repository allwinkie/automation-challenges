#!/usr/bin/python
# sqlalchemy section
import dbinit1 as dbcall
# python web fremework
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
    @cherrypy.expose
    def word(self, *args, **kwargs):
        if cherrypy.request.method == 'PUT':
            return self.RestPut(*args, **kwargs)
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
            return json.dumps( dbcall.Words.getAll() )
        name = args[0]
        
        cnt = dbcall.Words.getWordCount(name)
        if cnt == None:
            cnt = 0
        print "get request with no words to :/words/WORDNAME  gives the %s == %s" % (name, cnt)
        return json.dumps( {name: cnt} )
        

    def RestPut(self, *args, **kwargs):
        try:
            WORDNAME = urllib.unquote(args[0])
        except:
            raise cherrypy.HTTPError(501, 'Invalid URL, must specify WORDNAME')
        
        try:
            reqObj = json.loads(cherrypy.request.body.read())
        except:
            raise cherrypy.HTTPError(501, 'Invalid JSON body.')
        
        if type(reqObj) != dict:
            raise cherrypy.HTTPError(501, 'Invalid JSON data structure. Expecting type hash.')
        
        if not 'word' in reqObj:
            raise cherrypy.HTTPError(501, "Expecting hash key 'word' in JSON body, but wasn't found")
        
        if not len( reqObj['word'].split() ) == 1:
            raise cherrypy.HTTPError(501, 'PUT requests must be one word in length')
        
        if not len( WORDNAME.split() ) == 1:
            raise cherrypy.HTTPError(501, 'PUT requests must be one word in length')
        
        for _char in reqObj['word']:
            if _char in restrictedCars:
                raise cherrypy.HTTPError(501, '%s is not a word. Contains invalid character.' % reqObj['word'] )
            
        for _char in WORDNAME:
            if _char in restrictedCars:
                raise cherrypy.HTTPError(501, '%s restricted.' % WORDNAME )
            
        cnt = dbcall.Words.putWord(reqObj['word'])
        cnt = dbcall.Words.putWord(WORDNAME)
        
        
    
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
    
