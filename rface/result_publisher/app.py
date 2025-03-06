from flask import Flask, request, jsonify

class ResultPublisher:
  _instance = None

  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super(ResultPublisher, cls).__new__(cls, *args, **kwargs)
      cls._instance.__init_instance()
    return cls._instance

  def __init_instance(self):
    self.app = Flask(__name__)

  def add_route(self, route, handler):
    self.app.add_url_rule(route, view_func=handler)

  def run(self, host="0.0.0.0", port=5000, debug=False):
    self.app.run(host=host, port=port, debug=debug)