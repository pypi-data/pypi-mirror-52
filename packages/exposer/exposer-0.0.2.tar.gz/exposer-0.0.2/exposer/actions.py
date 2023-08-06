class BaseAction(object):
    starts_with = "<"
    method_seperator = "-"
    action_pointer = "@"
    instance_pointer = "#"
    ends_with = ">"

    def __init__(self, action):
        self.action = action

    def __call__(self, *args, **kwargs):
        return self.action(*args, **kwargs)

    def __repr__(self):
        hsh = ""
        if hasattr(self.action, "__qualname__"):
            hsh = (
                str(self.action_pointer)
                .join(self.action.__qualname__.split("."))
                .lower()
            )

        if hasattr(self.action, "__self__"):
            tmp = hsh.split(str(self.action_pointer))
            hsh = (
                str(self.action_pointer).join(
                    [
                        str(self.method_seperator).join(
                            tmp[0:-1]
                        ),
                        str(tmp[-1]),
                    ]
                )
                + str(self.instance_pointer)
                + str(self.action.__self__)
            )
        hsh = (
            str(self.starts_with)
            + hsh
            + str(self.ends_with)
        )
        return hsh


class Action(BaseAction):
    pass


class CliAction(BaseAction):
    starts_with = ""
    method_seperator = ":"
    action_pointer = ":"
    instance_pointer = ":"
    ends_with = ""


class PathAction(BaseAction):
    starts_with = "/"
    method_seperator = "/"
    action_pointer = "/"
    instance_pointer = "/"
    ends_with = ""
