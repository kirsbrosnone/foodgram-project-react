from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminAuthorOrReadOnly(BasePermission):
    """Права доступа: автор, админ или аноним(только для чтения)."""

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif obj.author == request.user or request.user.is_staff:
            return True
        return False


class IsAuthor(BasePermission):
    """Права доступа: автор."""

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(obj.author == request.user)
