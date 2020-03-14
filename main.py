import cherrypy
import traceback

from cherrypy.lib.static import serve_file

from screenshot import processConfig
import sys

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
        except Exception:
            error_msg = traceback.format_exc()
            return {"Error": str(error_msg)}
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
        },
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080
        }
    }
    cherrypy.quickstart(HelloWorld(), "/", conf)