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

    id = 257

    def __init__(self, answer):
        self.answer = answer
        self.Binary = self._Binary(self)

    @classmethod
    async def parse_bytes(cls, answer, read_len):
        # TODO: bytes parser
        instance = cls(answer)
        instance.critical = bool(answer.message.stream.read(f'uint:8'))
        instance.tag_length = answer.message.stream.read(f'uint:8')
        str_tag = answer.message.stream.read(f'bin:{instance.tag_length*8}')
        instance.tag = ''.join([chr(int(x, base=2)) for x in [str_tag[i:i + 8] for i in range(0, len(str_tag), 8)]])
        str_value = answer.message.stream.read(f'bin:{(read_len - instance.tag_length - 2) * 8}')
        instance.value = ''.join([chr(int(x, base=2)) for x in [str_value[i:i + 8] for i in range(0, len(str_value), 8)]])
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