
from django.db import models
from django.utils import six


class IntervalField(models.Field):
    description = 'Interval Field'

    def db_type(self, connection):
        return 'interval'

    def get_internal_type(self):
        return 'IntervalField'