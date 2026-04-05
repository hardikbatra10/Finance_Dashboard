from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """Full access — create, update, delete."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role == 'admin')


class IsAnalystOrAbove(BasePermission):
    """Read records + summaries. No writes."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated
                    and request.user.role in ('analyst', 'admin'))


class IsViewerOrAbove(BasePermission):
    """Any authenticated user can read dashboard summaries."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)