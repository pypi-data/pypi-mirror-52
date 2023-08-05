# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: admobilize/admprovider/v1alpha1/admprovider_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from admobilize.proto.admprovider.v1alpha1 import resources_pb2 as admobilize_dot_admprovider_dot_v1alpha1_dot_resources__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='admobilize/admprovider/v1alpha1/admprovider_service.proto',
  package='admobilize.admprovider.v1alpha1',
  syntax='proto3',
  serialized_options=_b('\n#com.admobilize.admprovider.v1alpha1B\027AdmproviderServiceProtoP\001\242\002\006ADMPRS\252\002\037AdMobilize.Admprovider.V1Alpha1'),
  serialized_pb=_b('\n9admobilize/admprovider/v1alpha1/admprovider_service.proto\x12\x1f\x61\x64mobilize.admprovider.v1alpha1\x1a\x1cgoogle/api/annotations.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a/admobilize/admprovider/v1alpha1/resources.proto\"\x85\x01\n\x10ProvisionRequest\x12\x1a\n\x12provisioning_token\x18\x01 \x01(\t\x12\x15\n\rmqtt_registry\x18\x02 \x01(\t\x12\x16\n\x0e\x61pplication_id\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65vice_name\x18\x04 \x01(\t\x12\x11\n\tdevice_id\x18\x05 \x01(\t\"S\n\x11ProvisionResponse\x12\x16\n\x0e\x61pplication_id\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65vice_name\x18\x02 \x01(\t\x12\x11\n\tdevice_id\x18\x03 \x01(\t\":\n\x11StreamLogsRequest\x12\x13\n\x0b\x61pplication\x18\x01 \x01(\t\x12\x10\n\x08loglevel\x18\x02 \x01(\t\"V\n\x12StreamLogsResponse\x12@\n\x0blog_message\x18\x01 \x01(\x0b\x32+.admobilize.admprovider.v1alpha1.LogMessage\"#\n\x12StreamStateRequest\x12\r\n\x05\x64\x65lay\x18\x01 \x01(\x04\"O\n\x12SendCommandRequest\x12\x39\n\x07\x63ommand\x18\x01 \x01(\x0b\x32(.admobilize.admprovider.v1alpha1.Command\"Y\n\x13SendCommandResponse\x12\x42\n\x08response\x18\x01 \x01(\x0b\x32\x30.admobilize.admprovider.v1alpha1.CommandResponse\"a\n\x11GetStatusResponse\x12\x1a\n\x12\x61pplication_status\x18\x01 \x01(\t\x12\x17\n\x0f\x64\x61tabase_status\x18\x02 \x01(\t\x12\x17\n\x0f\x63ritical_errors\x18\x03 \x03(\t2\xed\x07\n\x12\x41\x64mproviderService\x12t\n\tProvision\x12\x31.admobilize.admprovider.v1alpha1.ProvisionRequest\x1a\x32.admobilize.admprovider.v1alpha1.ProvisionResponse\"\x00\x12y\n\nStreamLogs\x12\x32.admobilize.admprovider.v1alpha1.StreamLogsRequest\x1a\x33.admobilize.admprovider.v1alpha1.StreamLogsResponse\"\x00\x30\x01\x12n\n\x0bStreamState\x12\x33.admobilize.admprovider.v1alpha1.StreamStateRequest\x1a&.admobilize.admprovider.v1alpha1.State\"\x00\x30\x01\x12R\n\x0cStreamFrames\x12\x16.google.protobuf.Empty\x1a&.admobilize.admprovider.v1alpha1.Frame\"\x00\x30\x01\x12L\n\x08GetState\x12\x16.google.protobuf.Empty\x1a&.admobilize.admprovider.v1alpha1.State\"\x00\x12Y\n\tGetStatus\x12\x16.google.protobuf.Empty\x1a\x32.admobilize.admprovider.v1alpha1.GetStatusResponse\"\x00\x12O\n\x03Run\x12..admobilize.admprovider.v1alpha1.Configuration\x1a\x16.google.protobuf.Empty\"\x00\x12U\n\tSetConfig\x12..admobilize.admprovider.v1alpha1.Configuration\x1a\x16.google.protobuf.Empty\"\x00\x12U\n\tGetConfig\x12\x16.google.protobuf.Empty\x1a..admobilize.admprovider.v1alpha1.Configuration\"\x00\x12z\n\x0bSendCommand\x12\x33.admobilize.admprovider.v1alpha1.SendCommandRequest\x1a\x34.admobilize.admprovider.v1alpha1.SendCommandResponse\"\x00\x42k\n#com.admobilize.admprovider.v1alpha1B\x17\x41\x64mproviderServiceProtoP\x01\xa2\x02\x06\x41\x44MPRS\xaa\x02\x1f\x41\x64Mobilize.Admprovider.V1Alpha1b\x06proto3')
  ,
  dependencies=[google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,admobilize_dot_admprovider_dot_v1alpha1_dot_resources__pb2.DESCRIPTOR,])




_PROVISIONREQUEST = _descriptor.Descriptor(
  name='ProvisionRequest',
  full_name='admobilize.admprovider.v1alpha1.ProvisionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='provisioning_token', full_name='admobilize.admprovider.v1alpha1.ProvisionRequest.provisioning_token', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mqtt_registry', full_name='admobilize.admprovider.v1alpha1.ProvisionRequest.mqtt_registry', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='application_id', full_name='admobilize.admprovider.v1alpha1.ProvisionRequest.application_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_name', full_name='admobilize.admprovider.v1alpha1.ProvisionRequest.device_name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_id', full_name='admobilize.admprovider.v1alpha1.ProvisionRequest.device_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=236,
  serialized_end=369,
)


_PROVISIONRESPONSE = _descriptor.Descriptor(
  name='ProvisionResponse',
  full_name='admobilize.admprovider.v1alpha1.ProvisionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='application_id', full_name='admobilize.admprovider.v1alpha1.ProvisionResponse.application_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_name', full_name='admobilize.admprovider.v1alpha1.ProvisionResponse.device_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='device_id', full_name='admobilize.admprovider.v1alpha1.ProvisionResponse.device_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=371,
  serialized_end=454,
)


_STREAMLOGSREQUEST = _descriptor.Descriptor(
  name='StreamLogsRequest',
  full_name='admobilize.admprovider.v1alpha1.StreamLogsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='application', full_name='admobilize.admprovider.v1alpha1.StreamLogsRequest.application', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='loglevel', full_name='admobilize.admprovider.v1alpha1.StreamLogsRequest.loglevel', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  serialized_start=456,
  serialized_end=514,
)


_STREAMLOGSRESPONSE = _descriptor.Descriptor(
  name='StreamLogsResponse',
  full_name='admobilize.admprovider.v1alpha1.StreamLogsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='log_message', full_name='admobilize.admprovider.v1alpha1.StreamLogsResponse.log_message', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=516,
  serialized_end=602,
)


_STREAMSTATEREQUEST = _descriptor.Descriptor(
  name='StreamStateRequest',
  full_name='admobilize.admprovider.v1alpha1.StreamStateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='delay', full_name='admobilize.admprovider.v1alpha1.StreamStateRequest.delay', index=0,
      number=1, type=4, cpp_type=4, label=1,
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
  serialized_start=604,
  serialized_end=639,
)


_SENDCOMMANDREQUEST = _descriptor.Descriptor(
  name='SendCommandRequest',
  full_name='admobilize.admprovider.v1alpha1.SendCommandRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='command', full_name='admobilize.admprovider.v1alpha1.SendCommandRequest.command', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=641,
  serialized_end=720,
)


_SENDCOMMANDRESPONSE = _descriptor.Descriptor(
  name='SendCommandResponse',
  full_name='admobilize.admprovider.v1alpha1.SendCommandResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='admobilize.admprovider.v1alpha1.SendCommandResponse.response', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
  serialized_start=722,
  serialized_end=811,
)


_GETSTATUSRESPONSE = _descriptor.Descriptor(
  name='GetStatusResponse',
  full_name='admobilize.admprovider.v1alpha1.GetStatusResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='application_status', full_name='admobilize.admprovider.v1alpha1.GetStatusResponse.application_status', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='database_status', full_name='admobilize.admprovider.v1alpha1.GetStatusResponse.database_status', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='critical_errors', full_name='admobilize.admprovider.v1alpha1.GetStatusResponse.critical_errors', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=813,
  serialized_end=910,
)

_STREAMLOGSRESPONSE.fields_by_name['log_message'].message_type = admobilize_dot_admprovider_dot_v1alpha1_dot_resources__pb2._LOGMESSAGE
_SENDCOMMANDREQUEST.fields_by_name['command'].message_type = admobilize_dot_admprovider_dot_v1alpha1_dot_resources__pb2._COMMAND
_SENDCOMMANDRESPONSE.fields_by_name['response'].message_type = admobilize_dot_admprovider_dot_v1alpha1_dot_resources__pb2._COMMANDRESPONSE
DESCRIPTOR.message_types_by_name['ProvisionRequest'] = _PROVISIONREQUEST
DESCRIPTOR.message_types_by_name['ProvisionResponse'] = _PROVISIONRESPONSE
DESCRIPTOR.message_types_by_name['StreamLogsRequest'] = _STREAMLOGSREQUEST
DESCRIPTOR.message_types_by_name['StreamLogsResponse'] = _STREAMLOGSRESPONSE
DESCRIPTOR.message_types_by_name['StreamStateRequest'] = _STREAMSTATEREQUEST
DESCRIPTOR.message_types_by_name['SendCommandRequest'] = _SENDCOMMANDREQUEST
DESCRIPTOR.message_types_by_name['SendCommandResponse'] = _SENDCOMMANDRESPONSE
DESCRIPTOR.message_types_by_name['GetStatusResponse'] = _GETSTATUSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ProvisionRequest = _reflection.GeneratedProtocolMessageType('ProvisionRequest', (_message.Message,), {
  'DESCRIPTOR' : _PROVISIONREQUEST,
  '__module__' : 'admobilize.admprovider.v1alpha1.admprovider_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.admprovider.v1alpha1.ProvisionRequest)
  })
_sym_db.RegisterMessage(ProvisionRequest)

ProvisionResponse = _reflection.GeneratedProtocolMessageType('ProvisionResponse', (_message.Message,), {
  'DESCRIPTOR' : _PROVISIONRESPONSE,
  '__module__' : 'admobilize.admprovider.v1alpha1.admprovider_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.admprovider.v1alpha1.ProvisionResponse)
  })
_sym_db.RegisterMessage(ProvisionResponse)

StreamLogsRequest = _reflection.GeneratedProtocolMessageType('StreamLogsRequest', (_message.Message,), {
  'DESCRIPTOR' : _STREAMLOGSREQUEST,
  '__module__' : 'admobilize.admprovider.v1alpha1.admprovider_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.admprovider.v1alpha1.StreamLogsRequest)
  })
_sym_db.RegisterMessage(StreamLogsRequest)

StreamLogsResponse = _reflection.GeneratedProtocolMessageType('StreamLogsResponse', (_message.Message,), {
  'DESCRIPTOR' : _STREAMLOGSRESPONSE,
  '__module__' : 'admobilize.admprovider.v1alpha1.admprovider_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.admprovider.v1alpha1.StreamLogsResponse)
  })
_sym_db.RegisterMessage(StreamLogsResponse)

StreamStateRequest = _reflection.GeneratedProtocolMessageType('StreamStateRequest', (_message.Message,), {
  'DESCRIPTOR' : _STREAMSTATEREQUEST,
  '__module__' : 'admobilize.admprovider.v1alpha1.admprovider_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.admprovider.v1alpha1.StreamStateRequest)
  })
_sym_db.RegisterMessage(StreamStateRequest)

SendCommandRequest = _reflection.GeneratedProtocolMessageType('SendCommandRequest', (_message.Message,), {
  'DESCRIPTOR' : _SENDCOMMANDREQUEST,
  '__module__' : 'admobilize.admprovider.v1alpha1.admprovider_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.admprovider.v1alpha1.SendCommandRequest)
  })
_sym_db.RegisterMessage(SendCommandRequest)

SendCommandResponse = _reflection.GeneratedProtocolMessageType('SendCommandResponse', (_message.Message,), {
  'DESCRIPTOR' : _SENDCOMMANDRESPONSE,
  '__module__' : 'admobilize.admprovider.v1alpha1.admprovider_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.admprovider.v1alpha1.SendCommandResponse)
  })
_sym_db.RegisterMessage(SendCommandResponse)

GetStatusResponse = _reflection.GeneratedProtocolMessageType('GetStatusResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETSTATUSRESPONSE,
  '__module__' : 'admobilize.admprovider.v1alpha1.admprovider_service_pb2'
  # @@protoc_insertion_point(class_scope:admobilize.admprovider.v1alpha1.GetStatusResponse)
  })
_sym_db.RegisterMessage(GetStatusResponse)


DESCRIPTOR._options = None

_ADMPROVIDERSERVICE = _descriptor.ServiceDescriptor(
  name='AdmproviderService',
  full_name='admobilize.admprovider.v1alpha1.AdmproviderService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=913,
  serialized_end=1918,
  methods=[
  _descriptor.MethodDescriptor(
    name='Provision',
    full_name='admobilize.admprovider.v1alpha1.AdmproviderService.Provision',
    index=0,
    containing_service=None,
    input_type=_PROVISIONREQUEST,
    output_type=_PROVISIONRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='StreamLogs',
    full_name='admobilize.admprovider.v1alpha1.AdmproviderService.StreamLogs',
    index=1,
    containing_service=None,
    input_type=_STREAMLOGSREQUEST,
    output_type=_STREAMLOGSRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='StreamState',
    full_name='admobilize.admprovider.v1alpha1.AdmproviderService.StreamState',
    index=2,
    containing_service=None,
    input_type=_STREAMSTATEREQUEST,
    output_type=admobilize_dot_admprovider_dot_v1alpha1_dot_resources__pb2._STATE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='StreamFrames',
    full_name='admobilize.admprovider.v1alpha1.AdmproviderService.StreamFrames',
    index=3,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=admobilize_dot_admprovider_dot_v1alpha1_dot_resources__pb2._FRAME,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetState',
    full_name='admobilize.admprovider.v1alpha1.AdmproviderService.GetState',
    index=4,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=admobilize_dot_admprovider_dot_v1alpha1_dot_resources__pb2._STATE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetStatus',
    full_name='admobilize.admprovider.v1alpha1.AdmproviderService.GetStatus',
    index=5,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_GETSTATUSRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Run',
    full_name='admobilize.admprovider.v1alpha1.AdmproviderService.Run',
    index=6,
    containing_service=None,
    input_type=admobilize_dot_admprovider_dot_v1alpha1_dot_resources__pb2._CONFIGURATION,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SetConfig',
    full_name='admobilize.admprovider.v1alpha1.AdmproviderService.SetConfig',
    index=7,
    containing_service=None,
    input_type=admobilize_dot_admprovider_dot_v1alpha1_dot_resources__pb2._CONFIGURATION,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetConfig',
    full_name='admobilize.admprovider.v1alpha1.AdmproviderService.GetConfig',
    index=8,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=admobilize_dot_admprovider_dot_v1alpha1_dot_resources__pb2._CONFIGURATION,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SendCommand',
    full_name='admobilize.admprovider.v1alpha1.AdmproviderService.SendCommand',
    index=9,
    containing_service=None,
    input_type=_SENDCOMMANDREQUEST,
    output_type=_SENDCOMMANDRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_ADMPROVIDERSERVICE)

DESCRIPTOR.services_by_name['AdmproviderService'] = _ADMPROVIDERSERVICE

# @@protoc_insertion_point(module_scope)
