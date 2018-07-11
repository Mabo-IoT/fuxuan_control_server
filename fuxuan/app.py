import falcon
from .data import Resource

api = application = falcon.API()

images = Resource()
api.add_route('/images', images)

