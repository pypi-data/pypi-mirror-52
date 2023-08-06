from logging import getLogger as getLocalLogger
from arrow import get as _

logger = getLocalLogger(__name__)


class UIntNumbersMixin:
    """UInt Numbers Mixin"""

    @staticmethod
    def to_uint256(value) -> int:
        return int(value * 10)

    @staticmethod
    def to_uint8(value) -> int:
        return int(value)


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