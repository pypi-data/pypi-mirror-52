from arrow import get as _
from web3 import Web3
import logging


# logger instance
logger = logging.getLogger(__name__)

class UIntNumbersMixin:
    """UInt Numbers Mixin"""

    @staticmethod
    def to_uint256(value) -> int:
        return int(value * 10)

    @staticmethod
    def to_uint8(value) -> int:
        return int(value)


class AddressMixin:
    """Address Mixin"""

    @staticmethod
    def checksum_address(address):
        return Web3.toChecksumAddress(address)


class EpochDatesMixin:
    """Epoch dates mixin"""

    @staticmethod
    def to_epoch(datetime):
        """Convert DateTime in Epoch timestamp"""
        _datetime = _(datetime)
        return int(_datetime.strftime('%s'))

    @staticmethod
    def from_epoch(datetime):
        """Convert Epoch to DateTime timestamp"""
        return _(datetime).format('YYYY-MM-DD HH:mm:ss')