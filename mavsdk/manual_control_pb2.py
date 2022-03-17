# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: manual_control/manual_control.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import mavsdk_options_pb2 as mavsdk__options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#manual_control/manual_control.proto\x12\x19mavsdk.rpc.manual_control\x1a\x14mavsdk_options.proto\"\x1d\n\x1bStartPositionControlRequest\"m\n\x1cStartPositionControlResponse\x12M\n\x15manual_control_result\x18\x01 \x01(\x0b\x32..mavsdk.rpc.manual_control.ManualControlResult\"\x1d\n\x1bStartAltitudeControlRequest\"m\n\x1cStartAltitudeControlResponse\x12M\n\x15manual_control_result\x18\x01 \x01(\x0b\x32..mavsdk.rpc.manual_control.ManualControlResult\"J\n\x1cSetManualControlInputRequest\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\t\n\x01z\x18\x03 \x01(\x02\x12\t\n\x01r\x18\x04 \x01(\x02\"n\n\x1dSetManualControlInputResponse\x12M\n\x15manual_control_result\x18\x01 \x01(\x0b\x32..mavsdk.rpc.manual_control.ManualControlResult\"\xcf\x02\n\x13ManualControlResult\x12\x45\n\x06result\x18\x01 \x01(\x0e\x32\x35.mavsdk.rpc.manual_control.ManualControlResult.Result\x12\x12\n\nresult_str\x18\x02 \x01(\t\"\xdc\x01\n\x06Result\x12\x12\n\x0eRESULT_UNKNOWN\x10\x00\x12\x12\n\x0eRESULT_SUCCESS\x10\x01\x12\x14\n\x10RESULT_NO_SYSTEM\x10\x02\x12\x1b\n\x17RESULT_CONNECTION_ERROR\x10\x03\x12\x0f\n\x0bRESULT_BUSY\x10\x04\x12\x19\n\x15RESULT_COMMAND_DENIED\x10\x05\x12\x12\n\x0eRESULT_TIMEOUT\x10\x06\x12\x1d\n\x19RESULT_INPUT_OUT_OF_RANGE\x10\x07\x12\x18\n\x14RESULT_INPUT_NOT_SET\x10\x08\x32\xc1\x03\n\x14ManualControlService\x12\x89\x01\n\x14StartPositionControl\x12\x36.mavsdk.rpc.manual_control.StartPositionControlRequest\x1a\x37.mavsdk.rpc.manual_control.StartPositionControlResponse\"\x00\x12\x89\x01\n\x14StartAltitudeControl\x12\x36.mavsdk.rpc.manual_control.StartAltitudeControlRequest\x1a\x37.mavsdk.rpc.manual_control.StartAltitudeControlResponse\"\x00\x12\x90\x01\n\x15SetManualControlInput\x12\x37.mavsdk.rpc.manual_control.SetManualControlInputRequest\x1a\x38.mavsdk.rpc.manual_control.SetManualControlInputResponse\"\x04\x80\xb5\x18\x01\x42.\n\x18io.mavsdk.manual_controlB\x12ManualControlProtob\x06proto3')



_STARTPOSITIONCONTROLREQUEST = DESCRIPTOR.message_types_by_name['StartPositionControlRequest']
_STARTPOSITIONCONTROLRESPONSE = DESCRIPTOR.message_types_by_name['StartPositionControlResponse']
_STARTALTITUDECONTROLREQUEST = DESCRIPTOR.message_types_by_name['StartAltitudeControlRequest']
_STARTALTITUDECONTROLRESPONSE = DESCRIPTOR.message_types_by_name['StartAltitudeControlResponse']
_SETMANUALCONTROLINPUTREQUEST = DESCRIPTOR.message_types_by_name['SetManualControlInputRequest']
_SETMANUALCONTROLINPUTRESPONSE = DESCRIPTOR.message_types_by_name['SetManualControlInputResponse']
_MANUALCONTROLRESULT = DESCRIPTOR.message_types_by_name['ManualControlResult']
_MANUALCONTROLRESULT_RESULT = _MANUALCONTROLRESULT.enum_types_by_name['Result']
StartPositionControlRequest = _reflection.GeneratedProtocolMessageType('StartPositionControlRequest', (_message.Message,), {
  'DESCRIPTOR' : _STARTPOSITIONCONTROLREQUEST,
  '__module__' : 'manual_control.manual_control_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.manual_control.StartPositionControlRequest)
  })
_sym_db.RegisterMessage(StartPositionControlRequest)

StartPositionControlResponse = _reflection.GeneratedProtocolMessageType('StartPositionControlResponse', (_message.Message,), {
  'DESCRIPTOR' : _STARTPOSITIONCONTROLRESPONSE,
  '__module__' : 'manual_control.manual_control_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.manual_control.StartPositionControlResponse)
  })
_sym_db.RegisterMessage(StartPositionControlResponse)

StartAltitudeControlRequest = _reflection.GeneratedProtocolMessageType('StartAltitudeControlRequest', (_message.Message,), {
  'DESCRIPTOR' : _STARTALTITUDECONTROLREQUEST,
  '__module__' : 'manual_control.manual_control_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.manual_control.StartAltitudeControlRequest)
  })
_sym_db.RegisterMessage(StartAltitudeControlRequest)

StartAltitudeControlResponse = _reflection.GeneratedProtocolMessageType('StartAltitudeControlResponse', (_message.Message,), {
  'DESCRIPTOR' : _STARTALTITUDECONTROLRESPONSE,
  '__module__' : 'manual_control.manual_control_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.manual_control.StartAltitudeControlResponse)
  })
_sym_db.RegisterMessage(StartAltitudeControlResponse)

SetManualControlInputRequest = _reflection.GeneratedProtocolMessageType('SetManualControlInputRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETMANUALCONTROLINPUTREQUEST,
  '__module__' : 'manual_control.manual_control_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.manual_control.SetManualControlInputRequest)
  })
_sym_db.RegisterMessage(SetManualControlInputRequest)

SetManualControlInputResponse = _reflection.GeneratedProtocolMessageType('SetManualControlInputResponse', (_message.Message,), {
  'DESCRIPTOR' : _SETMANUALCONTROLINPUTRESPONSE,
  '__module__' : 'manual_control.manual_control_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.manual_control.SetManualControlInputResponse)
  })
_sym_db.RegisterMessage(SetManualControlInputResponse)

ManualControlResult = _reflection.GeneratedProtocolMessageType('ManualControlResult', (_message.Message,), {
  'DESCRIPTOR' : _MANUALCONTROLRESULT,
  '__module__' : 'manual_control.manual_control_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.manual_control.ManualControlResult)
  })
_sym_db.RegisterMessage(ManualControlResult)

_MANUALCONTROLSERVICE = DESCRIPTOR.services_by_name['ManualControlService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030io.mavsdk.manual_controlB\022ManualControlProto'
  _MANUALCONTROLSERVICE.methods_by_name['SetManualControlInput']._options = None
  _MANUALCONTROLSERVICE.methods_by_name['SetManualControlInput']._serialized_options = b'\200\265\030\001'
  _STARTPOSITIONCONTROLREQUEST._serialized_start=88
  _STARTPOSITIONCONTROLREQUEST._serialized_end=117
  _STARTPOSITIONCONTROLRESPONSE._serialized_start=119
  _STARTPOSITIONCONTROLRESPONSE._serialized_end=228
  _STARTALTITUDECONTROLREQUEST._serialized_start=230
  _STARTALTITUDECONTROLREQUEST._serialized_end=259
  _STARTALTITUDECONTROLRESPONSE._serialized_start=261
  _STARTALTITUDECONTROLRESPONSE._serialized_end=370
  _SETMANUALCONTROLINPUTREQUEST._serialized_start=372
  _SETMANUALCONTROLINPUTREQUEST._serialized_end=446
  _SETMANUALCONTROLINPUTRESPONSE._serialized_start=448
  _SETMANUALCONTROLINPUTRESPONSE._serialized_end=558
  _MANUALCONTROLRESULT._serialized_start=561
  _MANUALCONTROLRESULT._serialized_end=896
  _MANUALCONTROLRESULT_RESULT._serialized_start=676
  _MANUALCONTROLRESULT_RESULT._serialized_end=896
  _MANUALCONTROLSERVICE._serialized_start=899
  _MANUALCONTROLSERVICE._serialized_end=1348
# @@protoc_insertion_point(module_scope)
