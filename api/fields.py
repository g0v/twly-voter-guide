import json
from rest_framework import serializers


class Field(serializers.ReadOnlyField):
    def to_native(self, obj):
        return obj
