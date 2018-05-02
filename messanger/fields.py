from django.contrib.postgres.fields import JSONField
from django.db.models import TextField
from django.core.serializers.json import DjangoJSONEncoder

# https://docs.djangoproject.com/en/1.11/topics/serialization/
class DataJSONField(JSONField):
    def deserialize_ecma262_datetime(self, value):
        # https://www.ecma-international.org/ecma-262/5.1/#sec-15.9.1.15
        # value = 'YYYY-MM-DDTHH:mm:ss.sss[Z|([+|-]HH:mm)]'
        value = value.replace(':', '')
        if value.endswith('Z'):
            value = value.replace('Z', '+0000')

        from datetime import datetime
        format_ecma262  = '%Y-%m-%dT%H%M%S.%f%z'
        return datetime.strptime(value, format_ecma262)

    def parse_datetime(self, value):
        value = { k: self.deserialize_ecma262_datetime(v) for k, v in value.items() }
        return value

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return self.parse_datetime(value)

class FormattedTextField(TextField):
    def pre_save(self, model_instance, add):
        import textwrap
        fmt = textwrap.fill(model_instance.message, 55, replace_whitespace=False)
        setattr(model_instance,'message',  fmt)
        print(fmt)
        return getattr(model_instance, self.attname)
