import os
from wsgiref.simple_server import make_server
from pyramid.config import Configurator

if __name__ == '__main__':
    config = Configurator()
    config.include('pyramid_mako')
    config.add_route('index', '/')
    config.add_route('export', '/export.json')
    config.scan('tpr_3.views')
    
    app = config.make_wsgi_app()
    server = make_server(os.getenv('IP', '0.0.0.0'), int(os.getenv('PORT', 8080)), app)
    server.serve_forever()
