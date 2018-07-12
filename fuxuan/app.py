import multiprocessing
import falcon

# import gunicorn.app.base
# from gunicorn.six import iteritems

import waitress

from utils.set_logging import setup_logging
from utils.get_conf import get_config

from data import Control


# class GunicornApplication(gunicorn.app.base.Application):

#     def __init__(self, app, options=None):
#         self.options = options or {}
#         self.application = app
#         super(GunicornApplication, self).__init__()
    
#     def load_config(self):
#         config = dict([(key, value) for key, value in iteritems(self.options)
#                        if key in self.cfg.settings and value is not None])
#         for key, value in iteritems(config):
#             self.cfg.set(key.lower(), value)
    
#     def load(self):
#         return self.application


def main():
    conf = get_config('conf/conf.toml')

    log = setup_logging(conf['log'])

    api = application = falcon.API()

    log.debug(conf)
    log.debug(conf['redis'])
    

    api.add_route('/control', Control(conf['redis']))
    waitress.serve(api, host=conf['server']['host'], port=conf['server']['port'], _quiet=False)
    # server = GunicornApplication(api, conf['server']).run()
    # server = GunicornApplication(api, conf['server']).reload()

if __name__ == '__main__':
    main()
