from rest_framework import serializers
from authentication.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    receiver_name = serializers.ReadOnlyField(source='receiver.username')

    class Meta:
        model = Transaction
        fields = ('id','receiver_name','amount','time')