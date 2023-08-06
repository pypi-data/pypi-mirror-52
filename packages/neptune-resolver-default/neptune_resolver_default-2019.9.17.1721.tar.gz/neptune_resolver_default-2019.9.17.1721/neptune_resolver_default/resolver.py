import triton


class Resolver:

    def __init__(self, con):
        self.connector = con
        
    async def find(self, name, type, cls):
        for resolver in self.connector.resolvers:
            try:
                result = await triton.query(resolver, domain=name, record_type=type)
                return result.__dict__
            except Exception as e:
                print(e)
        return {}