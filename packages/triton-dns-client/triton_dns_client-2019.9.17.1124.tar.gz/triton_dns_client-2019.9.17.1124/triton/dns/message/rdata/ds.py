from bitstring import BitArray


class DS:
    key_tag: int
    protocol: int
    algorithm: int
    digest: str

    class _Binary:
        def __init__(self, ds: 'DS'):
            self.ds = ds

        @property
        def full(self):
            result = bin(self.ds.flags)[2:].zfill(16)
            result += bin(self.ds.protocol)[2:].zfill(8)
            result += bin(self.ds.algorithm)[2:].zfill(8)
            result += BitArray(bytes=self.ds.public_key).bin
            return result

    id = 1

    def __init__(self, answer):
        self.answer = answer
        self.Binary = self._Binary(self)

    @classmethod
    async def parse_bytes(cls, answer, read_len):
        instance = cls(answer)
        instance.key_tag = answer.message.stream.read(f'bin:16')
        instance.protocol = answer.message.stream.read(f'uint:8')
        instance.algorithm = answer.message.stream.read(f'uint:8')
        str_ = answer.message.stream.read(f'bin:{read_len - 4}')
        instance.public_key = ''.join([chr(int(x, base=2)) for x in [str[i:i + 8] for i in range(0, len(str_), 8)]])
        return instance

    @classmethod
    async def parse_dict(cls, answer, data):
        instance = cls(answer)
        instance.key_tag = data.get('key_tag')
        instance.algorithm = data.get('algorithm')
        instance.digest_type = data.get('digest_type')
        instance.digest = data.get('digest')
        return instance

    @property
    def __dict__(self):
        return {'flags': int(self.flags),
                'protocol': int(self.protocol),
                'algorithm': int(self.algorithm),
                'public_key': str(self.public_key)}
