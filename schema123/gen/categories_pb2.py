# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: categories.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import schema123.gen.types_pb2 as types__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x63\x61tegories.proto\x1a\x0btypes.proto\"(\n\x18PredictCategoriesRequest\x12\x0c\n\x04text\x18\x01 \x01(\t\"@\n\x19PredictCategoriesResponse\x12#\n\x06result\x18\x01 \x03(\x0b\x32\x13.CategoryPrediction2X\n\nCategories\x12J\n\x11PredictCategories\x12\x19.PredictCategoriesRequest\x1a\x1a.PredictCategoriesResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'categories_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PREDICTCATEGORIESREQUEST']._serialized_start=33
  _globals['_PREDICTCATEGORIESREQUEST']._serialized_end=73
  _globals['_PREDICTCATEGORIESRESPONSE']._serialized_start=75
  _globals['_PREDICTCATEGORIESRESPONSE']._serialized_end=139
  _globals['_CATEGORIES']._serialized_start=141
  _globals['_CATEGORIES']._serialized_end=229
# @@protoc_insertion_point(module_scope)
