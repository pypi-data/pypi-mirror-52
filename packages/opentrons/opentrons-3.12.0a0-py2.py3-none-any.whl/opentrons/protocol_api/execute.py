import inspect
import json
import logging
import pkgutil
import traceback
import sys
from typing import Any, Callable, Dict

import jsonschema  # type: ignore

from .contexts import ProtocolContext
from . import execute_v1, execute_v3
from opentrons import config

MODULE_LOG = logging.getLogger(__name__)

PROTOCOL_MALFORMED = """

A Python protocol for the OT2 must define a function called 'run' that takes a
single argument: the protocol context to call functions on. For instance, a run
function might look like this:

def run(ctx):
    ctx.comment('hello, world')

This function is called by the robot when the robot executes the protol.
This function is not present in the current protocol and must be added.
"""


class ExceptionInProtocolError(Exception):
    """ This exception wraps an exception that was raised from a protocol
    for proper error message formatting by the rpc, since it's only here that
    we can properly figure out formatting
    """
    def __init__(self, original_exc, original_tb, message, line):
        self.original_exc = original_exc
        self.original_tb = original_tb
        self.message = message
        self.line = line
        super().__init__(original_exc, original_tb, message, line)

    def __str__(self):
        return '{}{}: {}'.format(
            self.original_exc.__class__.__name__,
            ' [line {}]'.format(self.line) if self.line else '',
            self.message)


class MalformedProtocolError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self._msg + PROTOCOL_MALFORMED

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.message)


def _runfunc_ok(run_func: Any) -> Callable[[ProtocolContext], None]:
    if not callable(run_func):
        raise SyntaxError("No function 'run(ctx)' defined")
    sig = inspect.Signature.from_callable(run_func)
    if not sig.parameters:
        raise SyntaxError("Function 'run()' does not take any parameters")
    if len(sig.parameters) > 1:
        for name, param in list(sig.parameters.items())[1:]:
            if param.default == inspect.Parameter.empty:
                raise SyntaxError(
                    "Function 'run{}' must be called with more than one "
                    "argument but would be called as 'run(ctx)'"
                    .format(str(sig)))
    return run_func  # type: ignore


def _find_protocol_error(tb, proto_name):
    """Return the FrameInfo for the lowest frame in the traceback from the
    protocol.
    """
    tb_info = traceback.extract_tb(tb)
    for frame in reversed(tb_info):
        if frame.filename == proto_name:
            return frame
    else:
        raise KeyError


def _run_python(proto: Any, context: ProtocolContext):
    new_locs = locals()
    new_globs = globals()
    name = getattr(proto, 'co_filename', '<protocol>')
    exec(proto, new_globs, new_locs)
    # If the protocol is written correctly, it will have defined a function
    # like run(context: ProtocolContext). If so, that function is now in the
    # current scope.
    try:
        _runfunc_ok(new_locs.get('run'))
    except SyntaxError as se:
        raise MalformedProtocolError(str(se))
    new_globs.update(new_locs)
    try:
        exec('run(context)', new_globs, new_locs)
    except Exception as e:
        exc_type, exc_value, tb = sys.exc_info()
        try:
            frame = _find_protocol_error(tb, name)
        except KeyError:
            # No pretty names, just raise it
            raise e
        raise ExceptionInProtocolError(e, tb, str(e), frame.lineno)


def get_protocol_schema_version(protocol_json: Dict[Any, Any]) -> int:
    # v3 and above uses `schemaVersion: integer`
    version = protocol_json.get('schemaVersion')
    if version:
        return version
    # v1 uses 1.x.x and v2 uses 2.x.x
    legacyKebabVersion = protocol_json.get('protocol-schema')
    # No minor/patch schemas ever were released,
    # do not permit protocols with nonexistent schema versions to load
    if legacyKebabVersion == '1.0.0':
        return 1
    elif legacyKebabVersion == '2.0.0':
        return 2
    elif legacyKebabVersion:
        raise RuntimeError(
            f'No such schema version: "{legacyKebabVersion}". Did you mean ' +
            '"1.0.0" or "2.0.0"?')
    # no truthy value for schemaVersion or protocol-schema
    raise RuntimeError(
        'Could not determine schema version for protocol. ' +
        'Make sure there is a version number under "schemaVersion"')


def get_schema_for_protocol(protocol_json: Dict[Any, Any]) -> Dict[Any, Any]:
    version_num = get_protocol_schema_version(protocol_json)
    try:
        schema = pkgutil.get_data(
            'opentrons',
            f'shared_data/protocol/schemas/{version_num}.json')
    except FileNotFoundError:
        schema = None
    if not schema:
        raise RuntimeError('JSON Protocol schema "{}" does not exist'
                           .format(version_num))
    return json.loads(schema)


def validate_protocol(protocol_json: Dict[Any, Any]):
    protocol_schema = get_schema_for_protocol(protocol_json)

    # instruct schema how to resolve all $ref's used in protocol schemas
    labware_schema_v2 = json.loads(  # type: ignore
        pkgutil.get_data(
            'opentrons',
            'shared_data/labware/schemas/2.json'))

    resolver = jsonschema.RefResolver(
        protocol_schema.get('$id', ''),
        protocol_schema,
        store={
            "opentronsLabwareSchemaV2": labware_schema_v2
        })
    # do the validation
    jsonschema.validate(protocol_json, protocol_schema, resolver=resolver)


def run_protocol(protocol_code: Any = None,
                 protocol_json: Dict[Any, Any] = None,
                 simulate: bool = False,
                 context: ProtocolContext = None):
    """ Create a ProtocolRunner instance from one of a variety of protocol
    sources.

    :param protocol_bytes: If the protocol is a Python protocol, pass the
    file contents here.
    :param protocol_json: If the protocol is a json file, pass the contents
    here.
    :param simulate: True to simulate; False to execute. If this is not an
    OT2, ``simulate`` will be forced ``True``.
    :param context: The context to use. If ``None``, create a new
    ProtocolContext.
    """
    if not config.IS_ROBOT:
        simulate = True # noqa - will be used later
    if None is context and simulate:
        true_context = ProtocolContext()
        true_context.home()
        MODULE_LOG.info("Generating blank protocol context for simulate")
    elif context:
        true_context = context
    else:
        raise RuntimeError(
            'Will not automatically generate hardware controller')
    if None is not protocol_code:
        _run_python(protocol_code, true_context)
    elif None is not protocol_json:
        protocol_version = get_protocol_schema_version(protocol_json)
        if protocol_version > 3:
            raise RuntimeError(
                f'JSON Protocol version {protocol_version} is not yet ' +
                'supported in this version of the API')

        validate_protocol(protocol_json)

        if protocol_version >= 3:
            ins = execute_v3.load_pipettes_from_json(
                true_context, protocol_json)
            lw = execute_v3.load_labware_from_json_defs(
                true_context, protocol_json)
            execute_v3.dispatch_json(true_context, protocol_json, ins, lw)
        else:
            ins = execute_v1.load_pipettes_from_json(
                true_context, protocol_json)
            lw = execute_v1.load_labware_from_json_loadnames(
                true_context, protocol_json)
            execute_v1.dispatch_json(true_context, protocol_json, ins, lw)
    else:
        raise RuntimeError("run_protocol must have either code or json")
