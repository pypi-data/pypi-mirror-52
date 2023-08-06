from infi.clickhouse_orm import engines

from .fields import DateField, DateTimeField, StringField, UInt64Field, BoolStringField
from .db import CLUSTER_NAME, Model, DistributedModel


class Recharges(Model):
    day = DateField()
    created_on = DateTimeField()
    profile_id = StringField()
    session_id = StringField()
    recharge_id = StringField()
    action = StringField()

    engine = engines.MergeTree(partition_key=('day',), order_by=('created_on', 'recharge_id'))


class RechargesDist(Recharges, DistributedModel):
    engine = engines.Distributed(CLUSTER_NAME)


class BattlepassProgress(Model):
    day = DateField(),
    created_on = DateTimeField()
    profile_id = StringField()
    session_id = StringField()
    battlepass_id = StringField()
    start_datetime = DateTimeField()
    step = UInt64Field()
    max_step = UInt64Field()
    source = StringField()
    difference = UInt64Field()
    new_progress = UInt64Field()
    has_premium = BoolStringField()
    league = UInt64Field(default=32)

    engine = engines.MergeTree(partition_key=('toYYYYMM(day)',), order_by=('created_on', 'battlepass_id'))


class BattlepassProgressDist(BattlepassProgress, DistributedModel):
    engine = engines.Distributed(CLUSTER_NAME)


class BattlepassWindowShown(Model):
    day = DateField(),
    created_on = DateTimeField()
    profile_id = StringField()
    session_id = StringField()
    battlepass_id = StringField()
    start_datetime = DateTimeField()
    step = UInt64Field()
    max_step = UInt64Field()
    has_premium = BoolStringField()
    league = UInt64Field(default=32)

    engine = engines.MergeTree(partition_key=('toYYYYMM(day)',), order_by=('created_on', 'battlepass_id'))


class BattlepassWindowShownDist(BattlepassWindowShown, DistributedModel):
    engine = engines.Distributed(CLUSTER_NAME)