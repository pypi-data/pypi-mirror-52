from ipaddress import IPv4Address


class A:
    class _Binary:
        def __init__(self, a: 'A'):
            self.a = a

        @property
        def full(self):
            return bin(int(self.a.address))[2:].zfill(8*4)
    id = 1

    def __init__(self, answer):
        self.answer = answer
        self.Binary = self._Binary(self)

    @classmethod
    async def parse_bytes(cls, answer, read_len):
        instance = cls(answer)
        instance.address = IPv4Address(answer.message.stream.read(f'uint:{read_len * 8}'))
        return instance

    @classmethod
    async def parse_dict(cls, answer, data):
        instance = cls(answer)
        try:
            instance.address = IPv4Address(data.get('address'))
        except AttributeError:
            instance.address = IPv4Address(data[0])
        return instance

    @property
    def __dict__(self):
        return {'address': int(self.address)}