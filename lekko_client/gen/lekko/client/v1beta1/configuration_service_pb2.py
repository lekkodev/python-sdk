# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: lekko/client/v1beta1/configuration_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0lekko/client/v1beta1/configuration_service.proto\x12\x14lekko.client.v1beta1\x1a\x19google/protobuf/any.proto\"K\n\rRepositoryKey\x12\x1d\n\nowner_name\x18\x01 \x01(\tR\townerName\x12\x1b\n\trepo_name\x18\x02 \x01(\tR\x08repoName\"\xb0\x02\n\x13GetBoolValueRequest\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12P\n\x07\x63ontext\x18\x02 \x03(\x0b\x32\x36.lekko.client.v1beta1.GetBoolValueRequest.ContextEntryR\x07\x63ontext\x12\x1c\n\tnamespace\x18\x03 \x01(\tR\tnamespace\x12>\n\x08repo_key\x18\x04 \x01(\x0b\x32#.lekko.client.v1beta1.RepositoryKeyR\x07repoKey\x1aW\n\x0c\x43ontextEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\x1b.lekko.client.v1beta1.ValueR\x05value:\x02\x38\x01\",\n\x14GetBoolValueResponse\x12\x14\n\x05value\x18\x01 \x01(\x08R\x05value\"\xae\x02\n\x12GetIntValueRequest\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12O\n\x07\x63ontext\x18\x02 \x03(\x0b\x32\x35.lekko.client.v1beta1.GetIntValueRequest.ContextEntryR\x07\x63ontext\x12\x1c\n\tnamespace\x18\x03 \x01(\tR\tnamespace\x12>\n\x08repo_key\x18\x04 \x01(\x0b\x32#.lekko.client.v1beta1.RepositoryKeyR\x07repoKey\x1aW\n\x0c\x43ontextEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\x1b.lekko.client.v1beta1.ValueR\x05value:\x02\x38\x01\"+\n\x13GetIntValueResponse\x12\x14\n\x05value\x18\x01 \x01(\x03R\x05value\"\xb2\x02\n\x14GetFloatValueRequest\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12Q\n\x07\x63ontext\x18\x02 \x03(\x0b\x32\x37.lekko.client.v1beta1.GetFloatValueRequest.ContextEntryR\x07\x63ontext\x12\x1c\n\tnamespace\x18\x03 \x01(\tR\tnamespace\x12>\n\x08repo_key\x18\x04 \x01(\x0b\x32#.lekko.client.v1beta1.RepositoryKeyR\x07repoKey\x1aW\n\x0c\x43ontextEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\x1b.lekko.client.v1beta1.ValueR\x05value:\x02\x38\x01\"-\n\x15GetFloatValueResponse\x12\x14\n\x05value\x18\x01 \x01(\x01R\x05value\"\xb4\x02\n\x15GetStringValueRequest\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12R\n\x07\x63ontext\x18\x02 \x03(\x0b\x32\x38.lekko.client.v1beta1.GetStringValueRequest.ContextEntryR\x07\x63ontext\x12\x1c\n\tnamespace\x18\x03 \x01(\tR\tnamespace\x12>\n\x08repo_key\x18\x04 \x01(\x0b\x32#.lekko.client.v1beta1.RepositoryKeyR\x07repoKey\x1aW\n\x0c\x43ontextEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\x1b.lekko.client.v1beta1.ValueR\x05value:\x02\x38\x01\".\n\x16GetStringValueResponse\x12\x14\n\x05value\x18\x01 \x01(\tR\x05value\"\xb2\x02\n\x14GetProtoValueRequest\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12Q\n\x07\x63ontext\x18\x02 \x03(\x0b\x32\x37.lekko.client.v1beta1.GetProtoValueRequest.ContextEntryR\x07\x63ontext\x12\x1c\n\tnamespace\x18\x03 \x01(\tR\tnamespace\x12>\n\x08repo_key\x18\x04 \x01(\x0b\x32#.lekko.client.v1beta1.RepositoryKeyR\x07repoKey\x1aW\n\x0c\x43ontextEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\x1b.lekko.client.v1beta1.ValueR\x05value:\x02\x38\x01\"y\n\x15GetProtoValueResponse\x12*\n\x05value\x18\x01 \x01(\x0b\x32\x14.google.protobuf.AnyR\x05value\x12\x34\n\x08value_v2\x18\x02 \x01(\x0b\x32\x19.lekko.client.v1beta1.AnyR\x07valueV2\"6\n\x03\x41ny\x12\x19\n\x08type_url\x18\x01 \x01(\tR\x07typeUrl\x12\x14\n\x05value\x18\x02 \x01(\x0cR\x05value\"\xb0\x02\n\x13GetJSONValueRequest\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12P\n\x07\x63ontext\x18\x02 \x03(\x0b\x32\x36.lekko.client.v1beta1.GetJSONValueRequest.ContextEntryR\x07\x63ontext\x12\x1c\n\tnamespace\x18\x03 \x01(\tR\tnamespace\x12>\n\x08repo_key\x18\x04 \x01(\x0b\x32#.lekko.client.v1beta1.RepositoryKeyR\x07repoKey\x1aW\n\x0c\x43ontextEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\x1b.lekko.client.v1beta1.ValueR\x05value:\x02\x38\x01\",\n\x14GetJSONValueResponse\x12\x14\n\x05value\x18\x01 \x01(\x0cR\x05value\"\x99\x01\n\x05Value\x12\x1f\n\nbool_value\x18\x01 \x01(\x08H\x00R\tboolValue\x12\x1d\n\tint_value\x18\x02 \x01(\x03H\x00R\x08intValue\x12#\n\x0c\x64ouble_value\x18\x03 \x01(\x01H\x00R\x0b\x64oubleValue\x12#\n\x0cstring_value\x18\x04 \x01(\tH\x00R\x0bstringValueB\x06\n\x04kind\"x\n\x0fRegisterRequest\x12>\n\x08repo_key\x18\x01 \x01(\x0b\x32#.lekko.client.v1beta1.RepositoryKeyR\x07repoKey\x12%\n\x0enamespace_list\x18\x02 \x03(\tR\rnamespaceList\"\x12\n\x10RegisterResponse\"\x13\n\x11\x44\x65registerRequest\"\x14\n\x12\x44\x65registerResponse2\xd5\x06\n\x14\x43onfigurationService\x12g\n\x0cGetBoolValue\x12).lekko.client.v1beta1.GetBoolValueRequest\x1a*.lekko.client.v1beta1.GetBoolValueResponse\"\x00\x12\x64\n\x0bGetIntValue\x12(.lekko.client.v1beta1.GetIntValueRequest\x1a).lekko.client.v1beta1.GetIntValueResponse\"\x00\x12j\n\rGetFloatValue\x12*.lekko.client.v1beta1.GetFloatValueRequest\x1a+.lekko.client.v1beta1.GetFloatValueResponse\"\x00\x12m\n\x0eGetStringValue\x12+.lekko.client.v1beta1.GetStringValueRequest\x1a,.lekko.client.v1beta1.GetStringValueResponse\"\x00\x12j\n\rGetProtoValue\x12*.lekko.client.v1beta1.GetProtoValueRequest\x1a+.lekko.client.v1beta1.GetProtoValueResponse\"\x00\x12g\n\x0cGetJSONValue\x12).lekko.client.v1beta1.GetJSONValueRequest\x1a*.lekko.client.v1beta1.GetJSONValueResponse\"\x00\x12[\n\x08Register\x12%.lekko.client.v1beta1.RegisterRequest\x1a&.lekko.client.v1beta1.RegisterResponse\"\x00\x12\x61\n\nDeregister\x12\'.lekko.client.v1beta1.DeregisterRequest\x1a(.lekko.client.v1beta1.DeregisterResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'lekko.client.v1beta1.configuration_service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETBOOLVALUEREQUEST_CONTEXTENTRY._options = None
  _GETBOOLVALUEREQUEST_CONTEXTENTRY._serialized_options = b'8\001'
  _GETINTVALUEREQUEST_CONTEXTENTRY._options = None
  _GETINTVALUEREQUEST_CONTEXTENTRY._serialized_options = b'8\001'
  _GETFLOATVALUEREQUEST_CONTEXTENTRY._options = None
  _GETFLOATVALUEREQUEST_CONTEXTENTRY._serialized_options = b'8\001'
  _GETSTRINGVALUEREQUEST_CONTEXTENTRY._options = None
  _GETSTRINGVALUEREQUEST_CONTEXTENTRY._serialized_options = b'8\001'
  _GETPROTOVALUEREQUEST_CONTEXTENTRY._options = None
  _GETPROTOVALUEREQUEST_CONTEXTENTRY._serialized_options = b'8\001'
  _GETJSONVALUEREQUEST_CONTEXTENTRY._options = None
  _GETJSONVALUEREQUEST_CONTEXTENTRY._serialized_options = b'8\001'
  _globals['_REPOSITORYKEY']._serialized_start=101
  _globals['_REPOSITORYKEY']._serialized_end=176
  _globals['_GETBOOLVALUEREQUEST']._serialized_start=179
  _globals['_GETBOOLVALUEREQUEST']._serialized_end=483
  _globals['_GETBOOLVALUEREQUEST_CONTEXTENTRY']._serialized_start=396
  _globals['_GETBOOLVALUEREQUEST_CONTEXTENTRY']._serialized_end=483
  _globals['_GETBOOLVALUERESPONSE']._serialized_start=485
  _globals['_GETBOOLVALUERESPONSE']._serialized_end=529
  _globals['_GETINTVALUEREQUEST']._serialized_start=532
  _globals['_GETINTVALUEREQUEST']._serialized_end=834
  _globals['_GETINTVALUEREQUEST_CONTEXTENTRY']._serialized_start=396
  _globals['_GETINTVALUEREQUEST_CONTEXTENTRY']._serialized_end=483
  _globals['_GETINTVALUERESPONSE']._serialized_start=836
  _globals['_GETINTVALUERESPONSE']._serialized_end=879
  _globals['_GETFLOATVALUEREQUEST']._serialized_start=882
  _globals['_GETFLOATVALUEREQUEST']._serialized_end=1188
  _globals['_GETFLOATVALUEREQUEST_CONTEXTENTRY']._serialized_start=396
  _globals['_GETFLOATVALUEREQUEST_CONTEXTENTRY']._serialized_end=483
  _globals['_GETFLOATVALUERESPONSE']._serialized_start=1190
  _globals['_GETFLOATVALUERESPONSE']._serialized_end=1235
  _globals['_GETSTRINGVALUEREQUEST']._serialized_start=1238
  _globals['_GETSTRINGVALUEREQUEST']._serialized_end=1546
  _globals['_GETSTRINGVALUEREQUEST_CONTEXTENTRY']._serialized_start=396
  _globals['_GETSTRINGVALUEREQUEST_CONTEXTENTRY']._serialized_end=483
  _globals['_GETSTRINGVALUERESPONSE']._serialized_start=1548
  _globals['_GETSTRINGVALUERESPONSE']._serialized_end=1594
  _globals['_GETPROTOVALUEREQUEST']._serialized_start=1597
  _globals['_GETPROTOVALUEREQUEST']._serialized_end=1903
  _globals['_GETPROTOVALUEREQUEST_CONTEXTENTRY']._serialized_start=396
  _globals['_GETPROTOVALUEREQUEST_CONTEXTENTRY']._serialized_end=483
  _globals['_GETPROTOVALUERESPONSE']._serialized_start=1905
  _globals['_GETPROTOVALUERESPONSE']._serialized_end=2026
  _globals['_ANY']._serialized_start=2028
  _globals['_ANY']._serialized_end=2082
  _globals['_GETJSONVALUEREQUEST']._serialized_start=2085
  _globals['_GETJSONVALUEREQUEST']._serialized_end=2389
  _globals['_GETJSONVALUEREQUEST_CONTEXTENTRY']._serialized_start=396
  _globals['_GETJSONVALUEREQUEST_CONTEXTENTRY']._serialized_end=483
  _globals['_GETJSONVALUERESPONSE']._serialized_start=2391
  _globals['_GETJSONVALUERESPONSE']._serialized_end=2435
  _globals['_VALUE']._serialized_start=2438
  _globals['_VALUE']._serialized_end=2591
  _globals['_REGISTERREQUEST']._serialized_start=2593
  _globals['_REGISTERREQUEST']._serialized_end=2713
  _globals['_REGISTERRESPONSE']._serialized_start=2715
  _globals['_REGISTERRESPONSE']._serialized_end=2733
  _globals['_DEREGISTERREQUEST']._serialized_start=2735
  _globals['_DEREGISTERREQUEST']._serialized_end=2754
  _globals['_DEREGISTERRESPONSE']._serialized_start=2756
  _globals['_DEREGISTERRESPONSE']._serialized_end=2776
  _globals['_CONFIGURATIONSERVICE']._serialized_start=2779
  _globals['_CONFIGURATIONSERVICE']._serialized_end=3632
# @@protoc_insertion_point(module_scope)
