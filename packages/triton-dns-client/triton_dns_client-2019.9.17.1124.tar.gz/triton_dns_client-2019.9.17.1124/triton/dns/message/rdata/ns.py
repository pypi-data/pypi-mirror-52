from ipaddress import IPv4Address
from ..domains.domain import Domain


class NS:
    class _Binary:
        def __init__(self, ns: 'NS'):
            self.ns = ns

        @property
        def full(self):
            return Domain.sub_encode(self.ns.nsdname.label)

    id = 2

    def __init__(self, answer):
        self.answer = answer
        self.Binary = self._Binary(self)

    @classmethod
    async def parse_bytes(cls, answer, read_len):
        instance = cls(answer)
        instance.nsdname = Domain.decode(answer.message)
        return instance

    @classmethod
    async def parse_dict(cls, answer, data):
        instance = cls(answer)
        try:
            instance.nsdname = Domain(data.get('label', data.get('nsdname')), None)
        except AttributeError:
            instance.nsdname = Domain(data[2], None)
        return instance

    @property
    def __dict__(self):
        return {'nsdname': self.nsdname}