from rest_framework import serializers
from .models import FinancialRecord


class FinancialRecordSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model  = FinancialRecord
        fields = ('id', 'user', 'amount', 'record_type', 'category',
                  'date', 'notes', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than zero.')
        return value