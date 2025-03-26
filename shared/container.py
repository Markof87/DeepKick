class Container:
    def __init__(self):
        self._dependencies = {}

    def register(self, name, dependency):
        self._dependencies[name] = dependency

    def resolve(self, name):
        return self._dependencies.get(name)