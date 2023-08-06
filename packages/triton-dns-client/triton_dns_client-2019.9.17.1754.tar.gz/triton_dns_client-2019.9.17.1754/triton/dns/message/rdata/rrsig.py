from ipaddress import IPv4Address


class RRSIG:
    type_covered: int
    algorithm: int
    labels: int
    original_ttl: int
    signature_expiration: int
    signature_inception: int
    key_tag: int
    signers_name: str
    signature: bytes

    class _Binary:
        def __init__(self, rrsig: 'RRSIG'):
            self.rrsig = rrsig

        @property
        def full(self):
            result = format(self.rrsig.type_covered, 'b').zfill(16)
            result += format(self.rrsig.algorithm, 'b').zfill(8)
            result += format(self.rrsig.labels, 'b').zfill(8)
            result += format(self.rrsig.original_ttl, 'b').zfill(32)
            result += format(self.rrsig.signature_expiration, 'b').zfill(32)
            result += format(self.rrsig.signature_inception, 'b').zfill(32)
            result += format(self.rrsig.key_tag, 'b').zfill(16)
            for prt in self.rrsig.signers_name.split('.'):
                sig_name = ''.join([bin(i)[2:].zfill(8) for i in [ord(c) for c in prt]])
                result += f'{bin(int(len(sig_name) / 8))[2:].zfill(8)}{sig_name}'
            else:
                result += str().zfill(8)
            result += self.rrsig.signature
            return result

        @property
        def without_signature(self):
            result = format(self.rrsig.type_covered, 'b').zfill(16)
            result += format(self.rrsig.algorithm, 'b').zfill(8)
            result += format(self.rrsig.labels, 'b').zfill(8)
            result += format(self.rrsig.original_ttl, 'b').zfill(32)
            result += format(self.rrsig.signature_expiration, 'b').zfill(32)
            result += format(self.rrsig.signature_inception, 'b').zfill(32)
            result += format(self.rrsig.key_tag, 'b').zfill(16)
            for prt in self.rrsig.signers_name.split('.'):
                sig_name = ''.join([bin(i)[2:].zfill(8) for i in [ord(c) for c in prt]])
                result += f'{bin(int(len(sig_name) / 8))[2:].zfill(8)}{sig_name}'
            else:
                result += str().zfill(8)
            return result

    id = 1

    def __init__(self, answer):
        self.answer = answer
        self.Binary = self._Binary(self)

    @classmethod
    async def parse_bytes(cls, answer, read_len):
        instance = cls(answer)
        instance.address = IPv4Address(answer.message.stream.read(f'uint:{read_len}'))
        return instance

    @classmethod
    async def parse_dict(cls, answer, data):
        instance = cls(answer)
        instance.type_covered = data.get('type_covered')
        instance.algorithm = data.get('algorithm')
        instance.labels = data.get('labels')
        instance.original_ttl = data.get('original_ttl')
        instance.signature_expiration = data.get('signature_expiration')
        instance.signature_inception = data.get('signature_inception')
        instance.key_tag = data.get('key_tag')
        instance.signers_name = data.get('signers_name')
        instance.signature = data.get('signature')
        return instance

    @property
    def __dict__(self):
        return {'type_covered': int(self.type_covered),
                'algorithm': int(self.algorithm),
                'labels': int(self.labels),
                'original_ttl': int(self.original_ttl),
                'signature_expiration': int(self.signature_expiration),
                'signature_inception': int(self.signature_inception),
                'key_tag': int(self.key_tag),
                'signers_name': str(self.signers_name),
                'signature': str(self.signature)}