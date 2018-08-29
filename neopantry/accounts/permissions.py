# Third-party imports.
from rest_framework import permissions

__author__ = 'Jason Parent'


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, user):
        if request.user:
            return user == request.user
        return False
