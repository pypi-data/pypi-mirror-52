import falcon


class HomeResource(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
