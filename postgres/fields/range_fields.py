from django.db import models
from django import forms
from django.utils import six

from psycopg2._range import Range

# Monkey patch Range so that we get a a string that can
# be used to save.
def range_to_string(value):
    if value and not isinstance(value, six.string_types):
        lower, upper = value._bounds
        return '%s%s,%s%s' % (
            lower, value.lower or '', value.upper or '', upper
        )
    return value

Range.__unicode__ = range_to_string

class RangeField(models.Field):
    pass




class Int4RangeField(RangeField):
    def db_type(self, connection):
        return 'int4range'

    def get_internal_type(self):
        return 'Int4RangeField'



class RangeOverlapsLookup(models.Lookup):
    lookup_name = 'overlaps'

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s && %s' % (lhs, rhs), params


RangeField.register_lookup(RangeOverlapsLookup)