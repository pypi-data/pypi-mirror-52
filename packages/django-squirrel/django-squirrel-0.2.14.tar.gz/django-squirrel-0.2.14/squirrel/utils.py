from django.core.exceptions import ValidationError
from logging import getLogger as getLocalLogger
import jsonschema
import uuid
import json


logger = getLocalLogger(__name__)


class Encoder:
    """Encoder"""
    def encode(self, decoded_value, *args, **kwargs): ...


class Decoder:
    """Encoder"""
    def decode(self, decoded_value, *args, **kwargs): ...


class JSONRPCEncoder(Encoder):
    """JSON RPC 2.0 encoder"""

    def get_id(self) -> int: return 0

    def encode(self, decoded_value, **kwargs) -> (str, bytes):
        """Encode value to JSONRPC schema"""
        method = kwargs.pop('method', None)
        str_output = kwargs.pop('str_output', True)
        params = decoded_value if isinstance(decoded_value, (dict, list)) else [decoded_value]
        mid = self.get_id()
        res = json.dumps({'params': params, 'method': method, 'id': mid, 'jsonrpc': '2.0'})
        if not str_output:
            res = res.encode()
        return res


class JSONRPCDecoder(Decoder):
    """JSON RPC 2.0 decoder"""

    validation_schema = {
        'type': 'object',
        'properties':
            {
                'method': {'type': 'string'},
                'jsonrpc': {'type': 'string'},
            },
        'required': ['method', 'params', 'id', 'jsonrpc']
    }

    def decode(self, encoded_value, *args, **kwargs) -> dict:
        try:
            if isinstance(encoded_value, bytes):
                encoded_value = encoded_value.decode()
            obj_json_rpc = json.loads(encoded_value)
            jsonschema.validate(obj_json_rpc.copy(), self.validation_schema)
            return obj_json_rpc
        except Exception as e:
            raise ValueError('JSON-RPC Decode error. %s' % str(e))


class JSONRPCEncoderDecoder(JSONRPCDecoder, JSONRPCEncoder):
    """JSON RPC 2.0 Encoder/Decoder"""


def create_name(obj_name='contract') -> str:
    """Create object var_name"""
    return 'new_' + obj_name.capitalize() + '_' + uuid.uuid4().hex


def is_json_serializable(value) -> bool:
    """Is JSON Serializable?"""
    try:
        return json.loads(value) is not None
    except json.decoder.JSONDecodeError:
        raise ValidationError(f'No JSON serializable.')

