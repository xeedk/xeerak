from rest_framework import serializers
from plugins.native.models import Native

class NativeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Native
        fields = ('firstName', 'lastName','nativeName')


        def create(self, validated_data):
            return Native.objects.create(**validated_data)

