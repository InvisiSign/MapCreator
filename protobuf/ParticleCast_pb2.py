# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ParticleCast.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='ParticleCast.proto',
  package='referencepoint.proto',
  syntax='proto3',
  serialized_options=_b('\n\030com.referencepoint.proto'),
  serialized_pb=_b('\n\x12ParticleCast.proto\x12\x14referencepoint.proto\"!\n\x0b\x43\x61stSummary\x12\x12\n\nnum_states\x18\x01 \x01(\x05\"\x0f\n\rParticleState2o\n\x0cParticleCast\x12_\n\x11\x43\x61stParticleState\x12#.referencepoint.proto.ParticleState\x1a!.referencepoint.proto.CastSummary\"\x00(\x01\x42\x1a\n\x18\x63om.referencepoint.protob\x06proto3')
)




_CASTSUMMARY = _descriptor.Descriptor(
  name='CastSummary',
  full_name='referencepoint.proto.CastSummary',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='num_states', full_name='referencepoint.proto.CastSummary.num_states', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=44,
  serialized_end=77,
)


_PARTICLESTATE = _descriptor.Descriptor(
  name='ParticleState',
  full_name='referencepoint.proto.ParticleState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=79,
  serialized_end=94,
)

DESCRIPTOR.message_types_by_name['CastSummary'] = _CASTSUMMARY
DESCRIPTOR.message_types_by_name['ParticleState'] = _PARTICLESTATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CastSummary = _reflection.GeneratedProtocolMessageType('CastSummary', (_message.Message,), dict(
  DESCRIPTOR = _CASTSUMMARY,
  __module__ = 'ParticleCast_pb2'
  # @@protoc_insertion_point(class_scope:referencepoint.proto.CastSummary)
  ))
_sym_db.RegisterMessage(CastSummary)

ParticleState = _reflection.GeneratedProtocolMessageType('ParticleState', (_message.Message,), dict(
  DESCRIPTOR = _PARTICLESTATE,
  __module__ = 'ParticleCast_pb2'
  # @@protoc_insertion_point(class_scope:referencepoint.proto.ParticleState)
  ))
_sym_db.RegisterMessage(ParticleState)


DESCRIPTOR._options = None

_PARTICLECAST = _descriptor.ServiceDescriptor(
  name='ParticleCast',
  full_name='referencepoint.proto.ParticleCast',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=96,
  serialized_end=207,
  methods=[
  _descriptor.MethodDescriptor(
    name='CastParticleState',
    full_name='referencepoint.proto.ParticleCast.CastParticleState',
    index=0,
    containing_service=None,
    input_type=_PARTICLESTATE,
    output_type=_CASTSUMMARY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_PARTICLECAST)

DESCRIPTOR.services_by_name['ParticleCast'] = _PARTICLECAST

# @@protoc_insertion_point(module_scope)
