from rest_framework import generics, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import FinancialRecord
from .serializers import FinancialRecordSerializer
from .filters import FinancialRecordFilter
from users.permissions import IsAdmin, IsAnalystOrAbove, IsViewerOrAbove


class FinancialRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = FinancialRecordSerializer
    filterset_class  = FinancialRecordFilter
    filter_backends  = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields  = ['date', 'amount', 'created_at']

    def get_queryset(self):
        print(self.request.user)
        qs = FinancialRecord.objects.filter(is_deleted=False)
        # Non-admins see only their own records
        if self.request.user.role != 'admin':
            qs = qs.filter(user=self.request.user)
        return qs

    def get_permissions(self):
        if self.request.method == 'POST':
            # Only admins and analysts can create records
            return [IsAnalystOrAbove()]
        return [IsViewerOrAbove()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FinancialRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FinancialRecordSerializer

    def get_queryset(self):
        qs = FinancialRecord.objects.filter(is_deleted=False)
        if self.request.user.role != 'admin':
            qs = qs.filter(user=self.request.user)
        return qs

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH', 'DELETE'):
            return [IsAdmin()]
        return [IsAnalystOrAbove()]

    def perform_destroy(self, instance):
        # Soft delete — never hard delete
        instance.is_deleted = True
        instance.save()