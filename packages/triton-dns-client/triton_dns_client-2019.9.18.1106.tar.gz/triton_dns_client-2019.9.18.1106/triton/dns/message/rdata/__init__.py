from .a import A
from .opt import OPT
from .aaaa import AAAA
from .mx import MX
from .ns import NS
from .soa import SOA
from .txt import TXT
from .dnskey import DNSKEY
from .rrsig import RRSIG
from .caa import CAA

rdata_cls = {
    1: A,
    2: NS,
    6: SOA,
    15: MX,
    16: TXT,
    28: AAAA,
    41: OPT,
    46: RRSIG,
    48: DNSKEY,
    257: CAA,
}
