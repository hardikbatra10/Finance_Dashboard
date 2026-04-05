from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from datetime import date, timedelta

from records.models import FinancialRecord
from users.permissions import IsViewerOrAbove


class DashboardSummaryView(APIView):
    """
    GET /api/dashboard/summary/
    Returns totals, net balance, category breakdown, recent activity.
    Accessible to all authenticated users (viewer and above).
    """
    permission_classes = [IsViewerOrAbove]

    def get_queryset(self, user):
        qs = FinancialRecord.objects.filter(is_deleted=False)
        if user.role != 'admin':
            qs = qs.filter(user=user)
        return qs

    def get(self, request):
        qs = self.get_queryset(request.user)

        total_income  = qs.filter(record_type='income') \
                          .aggregate(total=Sum('amount'))['total'] or 0
        total_expense = qs.filter(record_type='expense') \
                          .aggregate(total=Sum('amount'))['total'] or 0
        net_balance   = total_income - total_expense

        # Category-wise totals
        category_totals = (
            qs.values('category', 'record_type')
              .annotate(total=Sum('amount'))
              .order_by('category')
        )

        # Recent 5 transactions
        recent = qs.order_by('-date', '-created_at').values(
            'id', 'amount', 'record_type', 'category', 'date', 'notes'
        )[:5]

        return Response({
            'total_income':   total_income,
            'total_expense':  total_expense,
            'net_balance':    net_balance,
            'category_totals': list(category_totals),
            'recent_activity': list(recent),
        })


class MonthlyTrendView(APIView):
    """
    GET /api/dashboard/trends/
    Returns monthly income vs expense for the last 6 months.
    Analyst and Admin only.
    """
    permission_classes = [IsViewerOrAbove]

    def get(self, request):
        from users.permissions import IsAnalystOrAbove
        if not IsAnalystOrAbove().has_permission(request, self):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Analysts and admins only.')

        six_months_ago = date.today() - timedelta(days=180)
        qs = FinancialRecord.objects.filter(
            is_deleted=False, date__gte=six_months_ago
        )
        if request.user.role != 'admin':
            qs = qs.filter(user=request.user)

        trends = (
            qs.annotate(month=TruncMonth('date'))
              .values('month', 'record_type')
              .annotate(total=Sum('amount'))
              .order_by('month')
        )

        return Response({'monthly_trends': list(trends)})