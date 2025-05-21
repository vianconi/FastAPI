from jinja2 import Environment
from jinja2 import FileSystemLoader
from wsgiref.simple_server import make_server


def application(env, start_response):
    headers = [("Content-Type", "text/html")]

    start_response("200 OK", headers)

    env = Environment(loader=FileSystemLoader("templates"))

    template = env.get_template("index.html")

    html = template.render({"title": "Servidor en Python", "name": "Cody"})

    return [bytes(html, "utf-8")]


server = make_server("localhost", 8000, application)
server.serve_forever()
