from rest_framework.permissions import BasePermission, SAFE_METHODS

class OptionalAuthenticationPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            auth_header = request.headers.get('Authorization', '')
            if auth_header:
                return request.user and request.user.is_authenticated
            return True
        return request.user and request.user.is_authenticated
