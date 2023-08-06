import re
import sys
import pprint


class Cli(object):
    def __init__(self, actions):
        self.actions = actions
        print(80 * "-")
        pprint.pprint(self.actions)
        print(80 * "-")
        self.argv = sys.argv

    def __call__(self):
        if len(self.argv) == 1:
            return 1
        else:
            if self.argv[1] in self.actions.keys():
                self.args = []
                self.kwargs = {}
                arg_flag = True
                for i in self.argv[2:]:
                    match = re.search(r"(\w*)=(.*)", i)
                    if match:
                        self.kwargs[
                            match.group(1)
                        ] = match.group(2)
                        arg_flag = False
                    else:
                        if arg_flag:
                            self.args.append(i)
                        else:
                            raise Exception(
                                "kwargs must placed end"
                            )
                result = self.actions[self.argv[1]](
                    *self.args, **self.kwargs
                )
                print(result)
            return None


class Wsgi(object):
    def __init__(self, actions):
        self.actions = actions
        pprint.pprint(self.actions)

    def __call__(self):
        def handler(environ, start_response):
            """Simplest possible application object"""
            status = "200 OK"
            response_headers = [
                ("Content-type", "text/plain")
            ]
            start_response(status, response_headers)

            result = ""
            if environ["PATH_INFO"] in self.actions.keys():
                self.args = []
                self.kwargs = {}
                arg_flag = True
                for i in environ["QUERY_STRING"].split(
                    "&"
                ):
                    match = re.search(r"(\w*)=(.*)", i)
                    if match:
                        self.kwargs[
                            match.group(1)
                        ] = match.group(2)
                        arg_flag = False
                    else:
                        if arg_flag:
                            self.args.append(i)
                        else:
                            raise Exception(
                                "kwargs must placed end"
                            )
                result = self.actions[
                    environ["PATH_INFO"]
                ](*self.args, **self.kwargs)
            return [str(result).encode()]
            return [
                "\n".encode().join(
                    [
                        kw.encode()
                        + str(":").encode()
                        + str(item).encode()
                        for kw, item in environ.items()
                    ]
                )
            ]

        return handler
