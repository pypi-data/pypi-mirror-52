from ..domains.domain import Domain


class SOA:
    class _Binary:
        def __init__(self, soa: 'SOA'):
            self.soa = soa

        @property
        def full(self):
            result = Domain.sub_encode(self.soa.mname.label)
            result += Domain.sub_encode(self.soa.rname.label)
            result += bin(int(self.soa.serial))[2:].zfill(32)
            result += bin(int(self.soa.refresh))[2:].zfill(32)
            result += bin(self.soa.retry)[2:].zfill(32)
            result += bin(self.soa.expire)[2:].zfill(32)
            result += bin(self.soa.minimum)[2:].zfill(32)
            return result

    id = 6

    def __init__(self, answer):
        self.answer = answer
        self.Binary = self._Binary(self)

    @classmethod
    async def parse_bytes(cls, answer, read_len):
        instance = cls(answer)
        instance.mname = Domain.decode(answer.message)
        instance.rname = Domain.decode(answer.message)
        instance.serial = answer.message.stream.read('uint:32')
        instance.refresh = answer.message.stream.read('uint:32')
        instance.retry = answer.message.stream.read('uint:32')
        instance.expire = answer.message.stream.read('uint:32')
        instance.minimum = answer.message.stream.read('uint:32')
        return instance

    @classmethod
    async def parse_dict(cls, answer, data):
        instance = cls(answer)
        instance.mname = Domain(data.get('mname'), None)
        instance.rname = Domain(data.get('rname'), None)
        instance.serial = data.get('serial')
        instance.refresh = data.get('refresh')
        instance.retry = data.get('retry')
        instance.expire = data.get('expire')
        instance.minimum = data.get('minimum')
        return instance

    @property
    def __dict__(self):
        return {'mname': self.mname,
                'rname': self.rname,
                'serial': self.serial,
                'refresh': self.refresh,
                'retry': self.retry,
                'expire': self.expire,
                'minimum': self.minimum}
