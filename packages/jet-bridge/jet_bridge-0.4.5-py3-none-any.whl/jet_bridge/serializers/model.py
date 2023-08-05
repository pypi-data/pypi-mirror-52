from sqlalchemy import inspect

from jet_bridge import fields
from jet_bridge.serializers.model_serializer import ModelSerializer

data_types = [
    {'query': 'VARCHAR', 'operator': 'startswith', 'date_type': fields.CharField},
    {'query': 'TEXT', 'operator': 'equals', 'date_type': fields.CharField},
    {'query': 'BOOLEAN', 'operator': 'equals', 'date_type': fields.BooleanField},
    {'query': 'INTEGER', 'operator': 'equals', 'date_type': fields.CharField},
    {'query': 'SMALLINT', 'operator': 'equals', 'date_type': fields.CharField},
    {'query': 'NUMERIC', 'operator': 'startswith', 'date_type': fields.CharField},
    {'query': 'VARCHAR', 'operator': 'startswith', 'date_type': fields.CharField},
    {'query': 'TIMESTAMP', 'operator': 'startswith', 'date_type': fields.CharField},
    {'query': 'INTEGER[]', 'operator': 'startswith', 'date_type': fields.ArrayField},
    {'query': 'JSON', 'operator': 'startswith', 'date_type': fields.JSONField},
    {'query': 'geometry', 'operator': 'startswith', 'date_type': fields.WKTField},
    {'query': 'geography', 'operator': 'startswith', 'date_type': fields.WKTField},
]
default_data_type = fields.CharField


def get_column_data_type(column):
    try:
        data_type = str(column.type)
    except:
        data_type = 'NullType'

    for rule in data_types:
        if rule['operator'] == 'equals' and data_type == rule['query']:
            return rule['date_type']
        elif rule['operator'] == 'startswith' and data_type[:len(rule['query'])] == rule['query']:
            return rule['date_type']

    return default_data_type


def map_column(column):
    date_type = get_column_data_type(column)
    kwargs = {}
    if column.primary_key:
        kwargs['read_only'] = True
    return (column.key, date_type(**kwargs))


def get_model_serializer(Model):
    mapper = inspect(Model)

    class CustomModelSerializer(ModelSerializer):
        class Meta:
            model = Model
            dynamic_fields = dict(map(map_column, mapper.columns))

    return CustomModelSerializer
