class FlaskAbstractBaseResource(AbstractBaseResource, BaseBlueprint):
    def __init__(self):
        super(FlaskAbstractBaseResource, self).__init__("test", __name__)

    def add_route(self, url, method, handler):
        self.route(url, methods=[method])(handler)