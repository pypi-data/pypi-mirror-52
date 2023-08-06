import re
import io
import sys
import pprint


class Cli(object):
    def __init__(self, actions):
        self.actions = actions
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
            return result


class Wsgi(object):
    def __init__(self, actions):
        self.actions = actions

    def __call__(self):
        def handler(environ, start_response):
            """Simplest possible application object"""
            status = "200 OK"
            response_headers = [
                ("Content-type", "text/plain")
            ]
            start_response(status, response_headers)

            result = ""
            action_input = io.StringIO()
            action_output = io.StringIO()
            action_error = io.StringIO()
            if environ["PATH_INFO"] in self.actions.keys():
                self.args = []
                self.kwargs = {}
                arg_flag = True
                for i in environ["QUERY_STRING"].split(
                    "&"
                ):
                    match = re.search(r"(\w*)=(.*)", i)
                    if i is "" or None:
                        continue
                    elif match:
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

                sys.stdin = action_input
                sys.stdout = action_output
                sys.stderr = action_error

                result = self.actions[
                    environ["PATH_INFO"]
                ](*self.args, **self.kwargs)

                sys.stdin = sys.__stdin__
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__

            return [str(action_output.getvalue()).encode()]
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
