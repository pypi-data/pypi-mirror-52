from ..domains.domain import Domain


class MX:
    class _Binary:
        def __init__(self, mx: 'MX'):
            self.mx = mx

        @property
        def full(self):
            result = bin(int(self.mx.preference))[2:].zfill(16)
            result += Domain.sub_encode(self.mx.exchange.label)
            return result

    id = 28

    def __init__(self, answer):
        self.answer = answer
        self.Binary = self._Binary(self)

    @classmethod
    async def parse_bytes(cls, answer, read_len):
        instance = cls(answer)
        instance.preference = answer.message.stream.read(f'uint:{2}')
        instance.exchange = Domain.decode(answer.message)
        return instance

    @classmethod
    async def parse_dict(cls, answer, data):
        instance = cls(answer)
        instance.preference = data.get('preference')
        instance.exchange = Domain(data.get('exchange'), None)
        print(instance.__dict__)
        return instance

    @property
    def __dict__(self):
        return {'preference': self.preference,
                'exchange': self.exchange.__dict__}