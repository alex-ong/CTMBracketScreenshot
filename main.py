import cherrypy
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
    cherrypy.quickstart(HelloWorld())