# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cart.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\ncart.proto\x12\x04\x63\x61rt\"?\n\x16GetOrCreateCartRequest\x12\x11\n\tuser_hash\x18\x01 \x01(\t\x12\x12\n\nbrand_hash\x18\x02 \x01(\t\"3\n\x17GetOrCreateCartResponse\x12\x18\n\x04\x63\x61rt\x18\x01 \x01(\x0b\x32\n.cart.Cart\")\n\x14GetCartDetailRequest\x12\x11\n\tcart_hash\x18\x01 \x01(\t\"U\n\x15GetCartDetailResponse\x12\x18\n\x04\x63\x61rt\x18\x01 \x01(\x0b\x32\n.cart.Cart\x12\"\n\ncart_items\x18\x02 \x03(\x0b\x32\x0e.cart.CartItem\"M\n\x10\x41\x64\x64ToCartRequest\x12\x11\n\tcart_hash\x18\x01 \x01(\t\x12\x14\n\x0cproduct_hash\x18\x02 \x01(\t\x12\x10\n\x08quantity\x18\x03 \x01(\x05\">\n\x19GetCartItemDetailResponse\x12!\n\tcart_item\x18\x01 \x01(\x0b\x32\x0e.cart.CartItem\"G\n\x19\x41pplyCartItemPromoRequest\x12\x16\n\x0e\x63\x61rt_item_hash\x18\x01 \x01(\t\x12\x12\n\npromo_hash\x18\x02 \x01(\t\">\n\x15\x41pplyCartPromoRequest\x12\x11\n\tcart_hash\x18\x01 \x01(\t\x12\x12\n\npromo_hash\x18\x02 \x01(\t\"/\n\x15RemoveCartItemRequest\x12\x16\n\x0e\x63\x61rt_item_hash\x18\x01 \x01(\t\")\n\x16RemoveCartItemResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"%\n\x10\x43learCartRequest\x12\x11\n\tcart_hash\x18\x01 \x01(\t\"$\n\x11\x43learCartResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\xb9\x01\n\x04\x43\x61rt\x12\x0c\n\x04hash\x18\x01 \x01(\t\x12\x11\n\tuser_hash\x18\x02 \x01(\t\x12\x12\n\nbrand_hash\x18\x03 \x01(\t\x12\x11\n\tis_active\x18\x04 \x01(\x08\x12\x12\n\ncreated_at\x18\x05 \x01(\t\x12\x12\n\nupdated_at\x18\x06 \x01(\t\x12\x13\n\x0b\x63oupon_code\x18\x07 \x01(\t\x12\x12\n\npromo_hash\x18\x08 \x01(\t\x12\x18\n\x10\x61vailable_promos\x18\t \x01(\t\"\xaa\x01\n\x08\x43\x61rtItem\x12\x0c\n\x04hash\x18\x01 \x01(\t\x12\x14\n\x0cproduct_hash\x18\x02 \x01(\t\x12\x10\n\x08quantity\x18\x03 \x01(\x05\x12\r\n\x05price\x18\x04 \x01(\x01\x12\x13\n\x0b\x63oupon_code\x18\x05 \x01(\t\x12\x12\n\npromo_hash\x18\x06 \x01(\t\x12\x16\n\x0emodified_price\x18\x07 \x01(\x01\x12\x18\n\x10\x61vailable_promos\x18\x08 \x01(\t2\x9c\x04\n\x0b\x43\x61rtService\x12N\n\x0fGetOrCreateCart\x12\x1c.cart.GetOrCreateCartRequest\x1a\x1d.cart.GetOrCreateCartResponse\x12H\n\rGetCartDetail\x12\x1a.cart.GetCartDetailRequest\x1a\x1b.cart.GetCartDetailResponse\x12\x44\n\tAddToCart\x12\x16.cart.AddToCartRequest\x1a\x1f.cart.GetCartItemDetailResponse\x12V\n\x12\x41pplyCartItemPromo\x12\x1f.cart.ApplyCartItemPromoRequest\x1a\x1f.cart.GetCartItemDetailResponse\x12J\n\x0e\x41pplyCartPromo\x12\x1b.cart.ApplyCartPromoRequest\x1a\x1b.cart.GetCartDetailResponse\x12K\n\x0eRemoveCartItem\x12\x1b.cart.RemoveCartItemRequest\x1a\x1c.cart.RemoveCartItemResponse\x12<\n\tClearCart\x12\x16.cart.ClearCartRequest\x1a\x17.cart.ClearCartResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cart_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_GETORCREATECARTREQUEST']._serialized_start=20
  _globals['_GETORCREATECARTREQUEST']._serialized_end=83
  _globals['_GETORCREATECARTRESPONSE']._serialized_start=85
  _globals['_GETORCREATECARTRESPONSE']._serialized_end=136
  _globals['_GETCARTDETAILREQUEST']._serialized_start=138
  _globals['_GETCARTDETAILREQUEST']._serialized_end=179
  _globals['_GETCARTDETAILRESPONSE']._serialized_start=181
  _globals['_GETCARTDETAILRESPONSE']._serialized_end=266
  _globals['_ADDTOCARTREQUEST']._serialized_start=268
  _globals['_ADDTOCARTREQUEST']._serialized_end=345
  _globals['_GETCARTITEMDETAILRESPONSE']._serialized_start=347
  _globals['_GETCARTITEMDETAILRESPONSE']._serialized_end=409
  _globals['_APPLYCARTITEMPROMOREQUEST']._serialized_start=411
  _globals['_APPLYCARTITEMPROMOREQUEST']._serialized_end=482
  _globals['_APPLYCARTPROMOREQUEST']._serialized_start=484
  _globals['_APPLYCARTPROMOREQUEST']._serialized_end=546
  _globals['_REMOVECARTITEMREQUEST']._serialized_start=548
  _globals['_REMOVECARTITEMREQUEST']._serialized_end=595
  _globals['_REMOVECARTITEMRESPONSE']._serialized_start=597
  _globals['_REMOVECARTITEMRESPONSE']._serialized_end=638
  _globals['_CLEARCARTREQUEST']._serialized_start=640
  _globals['_CLEARCARTREQUEST']._serialized_end=677
  _globals['_CLEARCARTRESPONSE']._serialized_start=679
  _globals['_CLEARCARTRESPONSE']._serialized_end=715
  _globals['_CART']._serialized_start=718
  _globals['_CART']._serialized_end=903
  _globals['_CARTITEM']._serialized_start=906
  _globals['_CARTITEM']._serialized_end=1076
  _globals['_CARTSERVICE']._serialized_start=1079
  _globals['_CARTSERVICE']._serialized_end=1619
# @@protoc_insertion_point(module_scope)
