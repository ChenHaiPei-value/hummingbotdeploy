# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: trade.proto
# Protobuf Python Version: 4.25.2
"""Generated protocol buffer code."""
from google.protobuf import (
    descriptor as _descriptor,
    descriptor_pool as _descriptor_pool,
    symbol_database as _symbol_database,
)
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0btrade.proto\x12\x05trade"J\n\x0b\x43redentials\x12\x15\n\raccess_key_id\x18\x01 \x01(\t\x12\x11\n\tsignature\x18\x02 \x01(\t\x12\x11\n\ttimestamp\x18\x03 \x01(\x04"\xcb\x01\n\x0cOrderRequest\x12\x1e\n\x03new\x18\x01 \x01(\x0b\x32\x0f.trade.NewOrderH\x00\x12$\n\x06\x63\x61ncel\x18\x02 \x01(\x0b\x32\x12.trade.CancelOrderH\x00\x12$\n\x06modify\x18\x03 \x01(\x0b\x32\x12.trade.ModifyOrderH\x00\x12%\n\theartbeat\x18\x04 \x01(\x0b\x32\x10.trade.HeartbeatH\x00\x12\x1f\n\x02mc\x18\x05 \x01(\x0b\x32\x11.trade.MassCancelH\x00\x42\x07\n\x05inner"\x99\x03\n\x08NewOrder\x12\x17\n\x0f\x63lient_order_id\x18\x01 \x01(\x04\x12\x12\n\nrequest_id\x18\x02 \x01(\x04\x12\x11\n\tmarket_id\x18\x03 \x01(\x04\x12\x12\n\x05price\x18\x04 \x01(\x04H\x00\x88\x01\x01\x12\x10\n\x08quantity\x18\x05 \x01(\x04\x12\x19\n\x04side\x18\x06 \x01(\x0e\x32\x0b.trade.Side\x12)\n\rtime_in_force\x18\x07 \x01(\x0e\x32\x12.trade.TimeInForce\x12$\n\norder_type\x18\x08 \x01(\x0e\x32\x10.trade.OrderType\x12\x15\n\rsubaccount_id\x18\t \x01(\x04\x12>\n\x15self_trade_prevention\x18\n \x01(\x0e\x32\x1a.trade.SelfTradePreventionH\x01\x88\x01\x01\x12"\n\tpost_only\x18\x0b \x01(\x0e\x32\x0f.trade.PostOnly\x12\x1c\n\x14\x63\x61ncel_on_disconnect\x18\x0c \x01(\x08\x42\x08\n\x06_priceB\x18\n\x16_self_trade_prevention"d\n\x0b\x43\x61ncelOrder\x12\x11\n\tmarket_id\x18\x01 \x01(\x04\x12\x17\n\x0f\x63lient_order_id\x18\x02 \x01(\x04\x12\x12\n\nrequest_id\x18\x03 \x01(\x04\x12\x15\n\rsubaccount_id\x18\x04 \x01(\x04"\x8b\x02\n\x0bModifyOrder\x12\x11\n\tmarket_id\x18\x01 \x01(\x04\x12\x17\n\x0f\x63lient_order_id\x18\x02 \x01(\x04\x12\x12\n\nrequest_id\x18\x03 \x01(\x04\x12\x11\n\tnew_price\x18\x04 \x01(\x04\x12\x14\n\x0cnew_quantity\x18\x05 \x01(\x04\x12\x15\n\rsubaccount_id\x18\x06 \x01(\x04\x12>\n\x15self_trade_prevention\x18\x07 \x01(\x0e\x32\x1a.trade.SelfTradePreventionH\x00\x88\x01\x01\x12"\n\tpost_only\x18\x08 \x01(\x0e\x32\x0f.trade.PostOnlyB\x18\n\x16_self_trade_prevention"\x86\x01\n\nMassCancel\x12\x15\n\rsubaccount_id\x18\x01 \x01(\x04\x12\x12\n\nrequest_id\x18\x02 \x01(\x04\x12\x16\n\tmarket_id\x18\x03 \x01(\x04H\x00\x88\x01\x01\x12\x1e\n\x04side\x18\x04 \x01(\x0e\x32\x0b.trade.SideH\x01\x88\x01\x01\x42\x0c\n\n_market_idB\x07\n\x05_side"2\n\tHeartbeat\x12\x12\n\nrequest_id\x18\x01 \x01(\x04\x12\x11\n\ttimestamp\x18\x02 \x01(\x04"\xcb\x03\n\rOrderResponse\x12%\n\x07new_ack\x18\x01 \x01(\x0b\x32\x12.trade.NewOrderAckH\x00\x12+\n\ncancel_ack\x18\x02 \x01(\x0b\x32\x15.trade.CancelOrderAckH\x00\x12+\n\nmodify_ack\x18\x03 \x01(\x0b\x32\x15.trade.ModifyOrderAckH\x00\x12+\n\nnew_reject\x18\x04 \x01(\x0b\x32\x15.trade.NewOrderRejectH\x00\x12\x31\n\rcancel_reject\x18\x05 \x01(\x0b\x32\x18.trade.CancelOrderRejectH\x00\x12\x31\n\rmodify_reject\x18\x06 \x01(\x0b\x32\x18.trade.ModifyOrderRejectH\x00\x12\x1b\n\x04\x66ill\x18\x07 \x01(\x0b\x32\x0b.trade.FillH\x00\x12%\n\theartbeat\x18\x08 \x01(\x0b\x32\x10.trade.HeartbeatH\x00\x12(\n\x08position\x18\t \x01(\x0b\x32\x14.trade.AssetPositionH\x00\x12/\n\x0fmass_cancel_ack\x18\n \x01(\x0b\x32\x14.trade.MassCancelAckH\x00\x42\x07\n\x05inner"\xe5\x02\n\x0bNewOrderAck\x12\x13\n\x0bmsg_seq_num\x18\x01 \x01(\x04\x12\x17\n\x0f\x63lient_order_id\x18\x02 \x01(\x04\x12\x12\n\nrequest_id\x18\x03 \x01(\x04\x12\x19\n\x11\x65xchange_order_id\x18\x04 \x01(\x04\x12\x11\n\tmarket_id\x18\x05 \x01(\x04\x12\x12\n\x05price\x18\x06 \x01(\x04H\x00\x88\x01\x01\x12\x10\n\x08quantity\x18\x07 \x01(\x04\x12\x19\n\x04side\x18\x08 \x01(\x0e\x32\x0b.trade.Side\x12)\n\rtime_in_force\x18\t \x01(\x0e\x32\x12.trade.TimeInForce\x12$\n\norder_type\x18\n \x01(\x0e\x32\x10.trade.OrderType\x12\x15\n\rtransact_time\x18\x0b \x01(\x04\x12\x15\n\rsubaccount_id\x18\x0c \x01(\x04\x12\x1c\n\x14\x63\x61ncel_on_disconnect\x18\r \x01(\x08\x42\x08\n\x06_price"\xeb\x02\n\x0e\x43\x61ncelOrderAck\x12\x13\n\x0bmsg_seq_num\x18\x01 \x01(\x04\x12\x17\n\x0f\x63lient_order_id\x18\x02 \x01(\x04\x12\x12\n\nrequest_id\x18\x03 \x01(\x04\x12\x15\n\rtransact_time\x18\x04 \x01(\x04\x12\x15\n\rsubaccount_id\x18\x05 \x01(\x04\x12,\n\x06reason\x18\x06 \x01(\x0e\x32\x1c.trade.CancelOrderAck.Reason\x12\x11\n\tmarket_id\x18\x07 \x01(\x04\x12\x19\n\x11\x65xchange_order_id\x18\x08 \x01(\x04"\x8c\x01\n\x06Reason\x12\x10\n\x0cUNCLASSIFIED\x10\x00\x12\x0e\n\nDISCONNECT\x10\x01\x12\r\n\tREQUESTED\x10\x02\x12\x07\n\x03IOC\x10\x03\x12\x0f\n\x0bSTP_RESTING\x10\x04\x12\x12\n\x0eSTP_AGGRESSING\x10\x05\x12\x0f\n\x0bMASS_CANCEL\x10\x06\x12\x12\n\x0ePOSITION_LIMIT\x10\x07"\x88\x02\n\x0eModifyOrderAck\x12\x13\n\x0bmsg_seq_num\x18\x01 \x01(\x04\x12\x17\n\x0f\x63lient_order_id\x18\x02 \x01(\x04\x12\x12\n\nrequest_id\x18\x03 \x01(\x04\x12\x15\n\rtransact_time\x18\x04 \x01(\x04\x12\x1a\n\x12remaining_quantity\x18\x05 \x01(\x04\x12\x15\n\rsubaccount_id\x18\x06 \x01(\x04\x12\x11\n\tmarket_id\x18\x07 \x01(\x04\x12\r\n\x05price\x18\x08 \x01(\x04\x12\x10\n\x08quantity\x18\t \x01(\x04\x12\x1b\n\x13\x63umulative_quantity\x18\n \x01(\x04\x12\x19\n\x11\x65xchange_order_id\x18\x0b \x01(\x04"\x87\x02\n\rMassCancelAck\x12\x13\n\x0bmsg_seq_num\x18\x01 \x01(\x04\x12\x15\n\rsubaccount_id\x18\x02 \x01(\x04\x12\x12\n\nrequest_id\x18\x03 \x01(\x04\x12\x15\n\rtransact_time\x18\x04 \x01(\x04\x12\x30\n\x06reason\x18\x06 \x01(\x0e\x32\x1b.trade.MassCancelAck.ReasonH\x00\x88\x01\x01\x12\x1d\n\x15total_affected_orders\x18\x07 \x01(\r"C\n\x06Reason\x12\x10\n\x0cUNCLASSIFIED\x10\x00\x12\x15\n\x11INVALID_MARKET_ID\x10\x01\x12\x10\n\x0cINVALID_SIDE\x10\x02\x42\t\n\x07_reason"\xb1\x07\n\x0eNewOrderReject\x12\x13\n\x0bmsg_seq_num\x18\x01 \x01(\x04\x12\x17\n\x0f\x63lient_order_id\x18\x02 \x01(\x04\x12\x12\n\nrequest_id\x18\x03 \x01(\x04\x12\x15\n\rtransact_time\x18\x04 \x01(\x04\x12\x15\n\rsubaccount_id\x18\x05 \x01(\x04\x12,\n\x06reason\x18\x06 \x01(\x0e\x32\x1c.trade.NewOrderReject.Reason\x12\x11\n\tmarket_id\x18\x07 \x01(\x04\x12\x12\n\x05price\x18\x08 \x01(\x04H\x00\x88\x01\x01\x12\x10\n\x08quantity\x18\t \x01(\x04\x12\x19\n\x04side\x18\n \x01(\x0e\x32\x0b.trade.Side\x12)\n\rtime_in_force\x18\x0b \x01(\x0e\x32\x12.trade.TimeInForce\x12$\n\norder_type\x18\x0c \x01(\x0e\x32\x10.trade.OrderType"\xd1\x04\n\x06Reason\x12\x10\n\x0cUNCLASSIFIED\x10\x00\x12\x14\n\x10INVALID_QUANTITY\x10\x01\x12\x15\n\x11INVALID_MARKET_ID\x10\x02\x12\x16\n\x12\x44UPLICATE_ORDER_ID\x10\x03\x12\x10\n\x0cINVALID_SIDE\x10\x04\x12\x19\n\x15INVALID_TIME_IN_FORCE\x10\x05\x12\x16\n\x12INVALID_ORDER_TYPE\x10\x06\x12\x15\n\x11INVALID_POST_ONLY\x10\x07\x12!\n\x1dINVALID_SELF_TRADE_PREVENTION\x10\x08\x12\x12\n\x0eUNKNOWN_TRADER\x10\t\x12!\n\x1dPRICE_WITH_MARKET_LIMIT_ORDER\x10\n\x12\x1f\n\x1bPOST_ONLY_WITH_MARKET_ORDER\x10\x0b\x12\x1e\n\x1aPOST_ONLY_WITH_INVALID_TIF\x10\x0c\x12\x1a\n\x16\x45XCEEDED_SPOT_POSITION\x10\r\x12\x1d\n\x19NO_OPPOSING_RESTING_ORDER\x10\x0e\x12\x19\n\x15POST_ONLY_WOULD_TRADE\x10\x0f\x12\x16\n\x12\x44ID_NOT_FULLY_FILL\x10\x10\x12\x1e\n\x1aONLY_ORDER_CANCEL_ACCEPTED\x10\x11\x12$\n PROTECTION_PRICE_WOULD_NOT_TRADE\x10\x12\x12\x16\n\x12NO_REFERENCE_PRICE\x10\x13\x12\x15\n\x11SLIPPAGE_TOO_HIGH\x10\x14\x12\x16\n\x12OUTSIDE_PRICE_BAND\x10\x15\x42\x08\n\x06_price"\x8f\x02\n\x11\x43\x61ncelOrderReject\x12\x13\n\x0bmsg_seq_num\x18\x01 \x01(\x04\x12\x17\n\x0f\x63lient_order_id\x18\x02 \x01(\x04\x12\x12\n\nrequest_id\x18\x03 \x01(\x04\x12\x15\n\rtransact_time\x18\x04 \x01(\x04\x12\x15\n\rsubaccount_id\x18\x05 \x01(\x04\x12/\n\x06reason\x18\x06 \x01(\x0e\x32\x1f.trade.CancelOrderReject.Reason\x12\x11\n\tmarket_id\x18\x07 \x01(\x04"F\n\x06Reason\x12\x10\n\x0cUNCLASSIFIED\x10\x00\x12\x15\n\x11INVALID_MARKET_ID\x10\x01\x12\x13\n\x0fORDER_NOT_FOUND\x10\x02"\xf4\x03\n\x11ModifyOrderReject\x12\x13\n\x0bmsg_seq_num\x18\x01 \x01(\x04\x12\x17\n\x0f\x63lient_order_id\x18\x02 \x01(\x04\x12\x12\n\nrequest_id\x18\x03 \x01(\x04\x12\x15\n\rtransact_time\x18\x04 \x01(\x04\x12\x15\n\rsubaccount_id\x18\x05 \x01(\x04\x12/\n\x06reason\x18\x06 \x01(\x0e\x32\x1f.trade.ModifyOrderReject.Reason\x12\x11\n\tmarket_id\x18\x07 \x01(\x04"\xaa\x02\n\x06Reason\x12\x10\n\x0cUNCLASSIFIED\x10\x00\x12\x14\n\x10INVALID_QUANTITY\x10\x01\x12\x15\n\x11INVALID_MARKET_ID\x10\x02\x12\x13\n\x0fORDER_NOT_FOUND\x10\x03\x12\x0f\n\x0bINVALID_IFM\x10\x04\x12\x15\n\x11INVALID_POST_ONLY\x10\x05\x12!\n\x1dINVALID_SELF_TRADE_PREVENTION\x10\x06\x12\x12\n\x0eUNKNOWN_TRADER\x10\x07\x12\x1a\n\x16\x45XCEEDED_SPOT_POSITION\x10\x08\x12\x19\n\x15POST_ONLY_WOULD_TRADE\x10\t\x12\x1e\n\x1aONLY_ORDER_CANCEL_ACCEPTED\x10\x11\x12\x16\n\x12OUTSIDE_PRICE_BAND\x10\x0b"\xe8\x02\n\x04\x46ill\x12\x13\n\x0bmsg_seq_num\x18\x01 \x01(\x04\x12\x11\n\tmarket_id\x18\x02 \x01(\x04\x12\x17\n\x0f\x63lient_order_id\x18\x03 \x01(\x04\x12\x19\n\x11\x65xchange_order_id\x18\x04 \x01(\x04\x12\x12\n\nfill_price\x18\x05 \x01(\x04\x12\x15\n\rfill_quantity\x18\x06 \x01(\x04\x12\x17\n\x0fleaves_quantity\x18\x07 \x01(\x04\x12\x15\n\rtransact_time\x18\x08 \x01(\x04\x12\x15\n\rsubaccount_id\x18\t \x01(\x04\x12\x1b\n\x13\x63umulative_quantity\x18\n \x01(\x04\x12\x19\n\x04side\x18\x0b \x01(\x0e\x32\x0b.trade.Side\x12\x1b\n\x13\x61ggressor_indicator\x18\x0c \x01(\x08\x12+\n\tfee_ratio\x18\r \x01(\x0b\x32\x18.trade.FixedPointDecimal\x12\x10\n\x08trade_id\x18\x0e \x01(\x04"7\n\x11\x46ixedPointDecimal\x12\x10\n\x08mantissa\x18\x01 \x01(\x03\x12\x10\n\x08\x65xponent\x18\x02 \x01(\x05"|\n\rAssetPosition\x12\x15\n\rsubaccount_id\x18\x01 \x01(\x04\x12\x10\n\x08\x61sset_id\x18\x02 \x01(\x04\x12\x1e\n\x05total\x18\x03 \x01(\x0b\x32\x0f.trade.RawUnits\x12"\n\tavailable\x18\x04 \x01(\x0b\x32\x0f.trade.RawUnits"F\n\x08RawUnits\x12\r\n\x05word0\x18\x01 \x01(\x04\x12\r\n\x05word1\x18\x02 \x01(\x04\x12\r\n\x05word2\x18\x03 \x01(\x04\x12\r\n\x05word3\x18\x04 \x01(\x04"\x85\x01\n\tBootstrap\x12\x1b\n\x04\x64one\x18\x01 \x01(\x0b\x32\x0b.trade.DoneH\x00\x12\'\n\x07resting\x18\x02 \x01(\x0b\x32\x14.trade.RestingOrdersH\x00\x12)\n\x08position\x18\x03 \x01(\x0b\x32\x15.trade.AssetPositionsH\x00\x42\x07\n\x05inner"4\n\rRestingOrders\x12#\n\x06orders\x18\x01 \x03(\x0b\x32\x13.trade.RestingOrder"9\n\x0e\x41ssetPositions\x12\'\n\tpositions\x18\x01 \x03(\x0b\x32\x14.trade.AssetPosition"7\n\x04\x44one\x12\x1c\n\x14latest_transact_time\x18\x01 \x01(\x04\x12\x11\n\tread_only\x18\x02 \x01(\x08"\xe9\x02\n\x0cRestingOrder\x12\x17\n\x0f\x63lient_order_id\x18\x01 \x01(\x04\x12\x19\n\x11\x65xchange_order_id\x18\x02 \x01(\x04\x12\x11\n\tmarket_id\x18\x03 \x01(\x04\x12\r\n\x05price\x18\x04 \x01(\x04\x12\x16\n\x0eorder_quantity\x18\x05 \x01(\x04\x12\x19\n\x04side\x18\x06 \x01(\x0e\x32\x0b.trade.Side\x12)\n\rtime_in_force\x18\x07 \x01(\x0e\x32\x12.trade.TimeInForce\x12$\n\norder_type\x18\x08 \x01(\x0e\x32\x10.trade.OrderType\x12\x1a\n\x12remaining_quantity\x18\t \x01(\x04\x12\x11\n\trest_time\x18\n \x01(\x04\x12\x15\n\rsubaccount_id\x18\x0b \x01(\x04\x12\x1b\n\x13\x63umulative_quantity\x18\x0c \x01(\x04\x12\x1c\n\x14\x63\x61ncel_on_disconnect\x18\r \x01(\x08*\x18\n\x04Side\x12\x07\n\x03\x42ID\x10\x00\x12\x07\n\x03\x41SK\x10\x01*N\n\x0bTimeInForce\x12\x17\n\x13IMMEDIATE_OR_CANCEL\x10\x00\x12\x14\n\x10GOOD_FOR_SESSION\x10\x01\x12\x10\n\x0c\x46ILL_OR_KILL\x10\x02*D\n\tOrderType\x12\t\n\x05LIMIT\x10\x00\x12\x10\n\x0cMARKET_LIMIT\x10\x01\x12\x1a\n\x16MARKET_WITH_PROTECTION\x10\x02*V\n\x13SelfTradePrevention\x12\x12\n\x0e\x43\x41NCEL_RESTING\x10\x00\x12\x15\n\x11\x43\x41NCEL_AGGRESSING\x10\x01\x12\x14\n\x10\x41LLOW_SELF_TRADE\x10\x02*%\n\x08PostOnly\x12\x0c\n\x08\x44ISABLED\x10\x00\x12\x0b\n\x07\x45NABLED\x10\x01\x42\x12Z\x03go/\xaa\x02\nCube.Tradeb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "trade_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS is False:
    _globals["DESCRIPTOR"]._options = None
    _globals["DESCRIPTOR"]._serialized_options = b"Z\003go/\252\002\nCube.Trade"
    _globals["_SIDE"]._serialized_start = 6011
    _globals["_SIDE"]._serialized_end = 6035
    _globals["_TIMEINFORCE"]._serialized_start = 6037
    _globals["_TIMEINFORCE"]._serialized_end = 6115
    _globals["_ORDERTYPE"]._serialized_start = 6117
    _globals["_ORDERTYPE"]._serialized_end = 6185
    _globals["_SELFTRADEPREVENTION"]._serialized_start = 6187
    _globals["_SELFTRADEPREVENTION"]._serialized_end = 6273
    _globals["_POSTONLY"]._serialized_start = 6275
    _globals["_POSTONLY"]._serialized_end = 6312
    _globals["_CREDENTIALS"]._serialized_start = 22
    _globals["_CREDENTIALS"]._serialized_end = 96
    _globals["_ORDERREQUEST"]._serialized_start = 99
    _globals["_ORDERREQUEST"]._serialized_end = 302
    _globals["_NEWORDER"]._serialized_start = 305
    _globals["_NEWORDER"]._serialized_end = 714
    _globals["_CANCELORDER"]._serialized_start = 716
    _globals["_CANCELORDER"]._serialized_end = 816
    _globals["_MODIFYORDER"]._serialized_start = 819
    _globals["_MODIFYORDER"]._serialized_end = 1086
    _globals["_MASSCANCEL"]._serialized_start = 1089
    _globals["_MASSCANCEL"]._serialized_end = 1223
    _globals["_HEARTBEAT"]._serialized_start = 1225
    _globals["_HEARTBEAT"]._serialized_end = 1275
    _globals["_ORDERRESPONSE"]._serialized_start = 1278
    _globals["_ORDERRESPONSE"]._serialized_end = 1737
    _globals["_NEWORDERACK"]._serialized_start = 1740
    _globals["_NEWORDERACK"]._serialized_end = 2097
    _globals["_CANCELORDERACK"]._serialized_start = 2100
    _globals["_CANCELORDERACK"]._serialized_end = 2463
    _globals["_CANCELORDERACK_REASON"]._serialized_start = 2323
    _globals["_CANCELORDERACK_REASON"]._serialized_end = 2463
    _globals["_MODIFYORDERACK"]._serialized_start = 2466
    _globals["_MODIFYORDERACK"]._serialized_end = 2730
    _globals["_MASSCANCELACK"]._serialized_start = 2733
    _globals["_MASSCANCELACK"]._serialized_end = 2996
    _globals["_MASSCANCELACK_REASON"]._serialized_start = 2918
    _globals["_MASSCANCELACK_REASON"]._serialized_end = 2985
    _globals["_NEWORDERREJECT"]._serialized_start = 2999
    _globals["_NEWORDERREJECT"]._serialized_end = 3944
    _globals["_NEWORDERREJECT_REASON"]._serialized_start = 3341
    _globals["_NEWORDERREJECT_REASON"]._serialized_end = 3934
    _globals["_CANCELORDERREJECT"]._serialized_start = 3947
    _globals["_CANCELORDERREJECT"]._serialized_end = 4218
    _globals["_CANCELORDERREJECT_REASON"]._serialized_start = 4148
    _globals["_CANCELORDERREJECT_REASON"]._serialized_end = 4218
    _globals["_MODIFYORDERREJECT"]._serialized_start = 4221
    _globals["_MODIFYORDERREJECT"]._serialized_end = 4721
    _globals["_MODIFYORDERREJECT_REASON"]._serialized_start = 4423
    _globals["_MODIFYORDERREJECT_REASON"]._serialized_end = 4721
    _globals["_FILL"]._serialized_start = 4724
    _globals["_FILL"]._serialized_end = 5084
    _globals["_FIXEDPOINTDECIMAL"]._serialized_start = 5086
    _globals["_FIXEDPOINTDECIMAL"]._serialized_end = 5141
    _globals["_ASSETPOSITION"]._serialized_start = 5143
    _globals["_ASSETPOSITION"]._serialized_end = 5267
    _globals["_RAWUNITS"]._serialized_start = 5269
    _globals["_RAWUNITS"]._serialized_end = 5339
    _globals["_BOOTSTRAP"]._serialized_start = 5342
    _globals["_BOOTSTRAP"]._serialized_end = 5475
    _globals["_RESTINGORDERS"]._serialized_start = 5477
    _globals["_RESTINGORDERS"]._serialized_end = 5529
    _globals["_ASSETPOSITIONS"]._serialized_start = 5531
    _globals["_ASSETPOSITIONS"]._serialized_end = 5588
    _globals["_DONE"]._serialized_start = 5590
    _globals["_DONE"]._serialized_end = 5645
    _globals["_RESTINGORDER"]._serialized_start = 5648
    _globals["_RESTINGORDER"]._serialized_end = 6009
# @@protoc_insertion_point(module_scope)
