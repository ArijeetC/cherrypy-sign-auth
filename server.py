'''Main python module which contains all necessary classes and functions for server startup.
Server can be started by running this module directly.

'''


import os
import configparser
import json
import cherrypy



def jsonify_error(status, message, traceback, version): #pylint: disable=unused-argument
    '''Converts errors from HTML to JSON format.

    Args:
        status (str): HTTP response status code.
        message (str): Response message.
        traceback (str): Exception traceback.
        version (str): Version.

    Returns:
        A JSON string representation of the error message and status code.

    '''
    response = cherrypy.response
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'status': status, 'message': message})

class AppController(object):
    '''CherryPy controller/handler class for handling the home and health URLs.
    '''

    @cherrypy.expose()
    def index(self):
        '''Handler method for the /app/home URL.
        '''
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        return "Basic CherryPy Example"

    @cherrypy.expose()
    def health(self):
        '''Handler method for the /app/health URL.
        '''
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        return "RUNNING"


class Server(object):
    '''CherryPy server class containing all necessary server configurations,
       such as URL mappings to their respective handler methods, authentication settings,
       hostname and port.

    Args:
        host (str): Hostname for the server.
        port (int): Port number for the server.

    '''

    def __init__(self, host, port):

        conf = {
            '/app': {
                'error_page.default': jsonify_error,
                'tools.auth_sign.on': True,
                'tools.auth_sign.realm': host,
                'tools.auth_sign.key_file': 'keys/public.pem',
                'tools.auth_sign.debug': True,
            }

        }


        root = AppController()
        root.app = AppController()

        cherrypy.tree.mount(root=root, config=conf)


        cherrypy.server.socket_host = host
        cherrypy.server.socket_port = port
        cherrypy.server.thread_pool = 20
        self.engine = cherrypy.engine

    def run(self):
        '''Starts the CherryPy server.
        '''

        self.engine.start()

        self.engine.block()


if __name__ == '__main__':

    SERVER_HOST = "0.0.0.0"
    PORT = 8081

    Server(SERVER_HOST, PORT).run()
