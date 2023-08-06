from ipaddress import IPv4Address


class CAA:
    class _Binary:
        def __init__(self, caa: 'CAA'):
            self.caa = caa

        @property
        def full(self):
            result = format(self.caa.critical, 'b').zfill(8)
            result += format(len(self.caa.tag), 'b').zfill(8)
            result += ''.join([bin(i)[2:].zfill(8) for i in [ord(c) for c in self.caa.tag]])
            result += ''.join([bin(i)[2:].zfill(8) for i in [ord(c) for c in self.caa.value]])
            return result
    id = 1

    def __init__(self, answer):
        self.answer = answer
        self.Binary = self._Binary(self)

    @classmethod
    async def parse_bytes(cls, answer, read_len):
        # TODO: bytes parser
        instance = cls(answer)
        instance.address = IPv4Address(answer.message.stream.read(f'uint:{read_len}'))
        return instance

    @classmethod
    async def parse_dict(cls, answer, data):
        instance = cls(answer)
        instance.critical = data.get('critical')
        instance.tag = data.get('tag')
        instance.value = data.get('value')
        return instance

    @property
    def __dict__(self):
        return {'critical': int(self.critical),
                'tag': str(self.tag),
                'value': str(self.value)}