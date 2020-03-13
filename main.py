import cherrypy
from cherrypy.lib.static import serve_file

from screenshot import processConfig

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello World!"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    def api(self):        
        input_json = cherrypy.request.json
        try:
            result = processConfig(input_json)
        except:
            return {"Error":"Somewhere"}
        result = {"files":result}
        return result


if __name__ == '__main__':
    # enable file serving on the "output" directory
    import os
    
    fileServe = os.path.dirname(os.path.abspath(__file__))+'/output/'

    try:
        os.mkdir(fileServe)
    except:
        pass

    conf = {
        '/output': {
            'tools.staticdir.on' : True,
            'tools.staticdir.dir' : fileServe
        }
    }
    cherrypy.quickstart(HelloWorld(), "/", conf)