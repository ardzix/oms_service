# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: checkout.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x63heckout.proto\x12\x08\x63heckout\"=\n\x15\x43reateCheckoutRequest\x12\x11\n\tcart_hash\x18\x01 \x01(\t\x12\x11\n\tuser_hash\x18\x02 \x01(\t\"n\n\x15UpdateCheckoutRequest\x12\x0c\n\x04hash\x18\x01 \x01(\t\x12\x13\n\x0btotal_price\x18\x02 \x01(\x01\x12\x10\n\x08\x64iscount\x18\x03 \x01(\x01\x12\x0b\n\x03vat\x18\x04 \x01(\x01\x12\x13\n\x0b\x66inal_price\x18\x05 \x01(\x01\"%\n\x15\x44\x65leteCheckoutRequest\x12\x0c\n\x04hash\x18\x01 \x01(\t\")\n\x14ListCheckoutsRequest\x12\x11\n\tuser_hash\x18\x01 \x01(\t\"(\n\x18GetCheckoutDetailRequest\x12\x0c\n\x04hash\x18\x01 \x01(\t\"\xa3\x01\n\x10\x43heckoutResponse\x12\x0c\n\x04hash\x18\x01 \x01(\t\x12\x11\n\tuser_hash\x18\x02 \x01(\t\x12\x11\n\tcart_hash\x18\x03 \x01(\t\x12\x13\n\x0btotal_price\x18\x04 \x01(\x01\x12\x10\n\x08\x64iscount\x18\x05 \x01(\x01\x12\x0b\n\x03vat\x18\x06 \x01(\x01\x12\x13\n\x0b\x66inal_price\x18\x07 \x01(\x01\x12\x12\n\ncreated_at\x18\x08 \x01(\t\"r\n\x16\x43heckoutDetailResponse\x12,\n\x08\x63heckout\x18\x01 \x01(\x0b\x32\x1a.checkout.CheckoutResponse\x12*\n\x07invoice\x18\x02 \x01(\x0b\x32\x19.checkout.InvoiceResponse\"F\n\x15ListCheckoutsResponse\x12-\n\tcheckouts\x18\x01 \x03(\x0b\x32\x1a.checkout.CheckoutResponse\"M\n\x0fInvoiceResponse\x12\x16\n\x0einvoice_number\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x12\n\ncreated_at\x18\x03 \x01(\t\"\x07\n\x05\x45mpty2\xa0\x03\n\x0f\x43heckoutService\x12M\n\x0e\x43reateCheckout\x12\x1f.checkout.CreateCheckoutRequest\x1a\x1a.checkout.CheckoutResponse\x12P\n\rListCheckouts\x12\x1e.checkout.ListCheckoutsRequest\x1a\x1f.checkout.ListCheckoutsResponse\x12Y\n\x11GetCheckoutDetail\x12\".checkout.GetCheckoutDetailRequest\x1a .checkout.CheckoutDetailResponse\x12M\n\x0eUpdateCheckout\x12\x1f.checkout.UpdateCheckoutRequest\x1a\x1a.checkout.CheckoutResponse\x12\x42\n\x0e\x44\x65leteCheckout\x12\x1f.checkout.DeleteCheckoutRequest\x1a\x0f.checkout.Emptyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'checkout_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_CREATECHECKOUTREQUEST']._serialized_start=28
  _globals['_CREATECHECKOUTREQUEST']._serialized_end=89
  _globals['_UPDATECHECKOUTREQUEST']._serialized_start=91
  _globals['_UPDATECHECKOUTREQUEST']._serialized_end=201
  _globals['_DELETECHECKOUTREQUEST']._serialized_start=203
  _globals['_DELETECHECKOUTREQUEST']._serialized_end=240
  _globals['_LISTCHECKOUTSREQUEST']._serialized_start=242
  _globals['_LISTCHECKOUTSREQUEST']._serialized_end=283
  _globals['_GETCHECKOUTDETAILREQUEST']._serialized_start=285
  _globals['_GETCHECKOUTDETAILREQUEST']._serialized_end=325
  _globals['_CHECKOUTRESPONSE']._serialized_start=328
  _globals['_CHECKOUTRESPONSE']._serialized_end=491
  _globals['_CHECKOUTDETAILRESPONSE']._serialized_start=493
  _globals['_CHECKOUTDETAILRESPONSE']._serialized_end=607
  _globals['_LISTCHECKOUTSRESPONSE']._serialized_start=609
  _globals['_LISTCHECKOUTSRESPONSE']._serialized_end=679
  _globals['_INVOICERESPONSE']._serialized_start=681
  _globals['_INVOICERESPONSE']._serialized_end=758
  _globals['_EMPTY']._serialized_start=760
  _globals['_EMPTY']._serialized_end=767
  _globals['_CHECKOUTSERVICE']._serialized_start=770
  _globals['_CHECKOUTSERVICE']._serialized_end=1186
# @@protoc_insertion_point(module_scope)
