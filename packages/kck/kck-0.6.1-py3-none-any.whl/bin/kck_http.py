#!/usr/bin/env python
# import tornado.escape
import tornado.ioloop
from tornado.options import define, options, parse_command_line

from kck.lib.http_service import KCKHTTPServer

# define("port", default=6001, help="run on the given port", type=int)
# define("debug", default=True, help="run in debug mode")

def main():
    parse_command_line()
    app = KCKHTTPServer.get_instance()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
