from .resolver import Resolver


class Connection:

    def __init__(self, loop, resolvers):
        self.loop = loop
        self.resolvers = resolvers
        self.Resolver = Resolver(self)

