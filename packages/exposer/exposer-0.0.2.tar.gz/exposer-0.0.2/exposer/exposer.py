from .actions import CliAction
from .targets import Cli


class Encapsulate(object):
    value = None

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        self.value = value

    def __delete__(self, instance):
        del self


class Exposer(object):
    count = 0
    action = None
    name = None

    def __set_name__(self, owner, name):
        self.name = name
        self.help = self(self.help)

    def __init__(self, action=CliAction, target=Cli):
        Exposer.count += 1
        self.live_id = Exposer.count
        self.actions = {}
        self.action = action
        self.target = target

    def __repr__(self):
        return str(self.name)

    def rename(self, name, newname):
        action = self.actions.pop(name)
        self.actions[newname] = action

    def help(self):
        """show this output"""
        for kw, val in self.actions.items():
            print(kw)

    def __call__(self, function):
        action = self.action(function)
        self.actions[str(action)] = action
        return function

    def expose(self):
        self.app = self.target(self.actions)
        return self.app()
