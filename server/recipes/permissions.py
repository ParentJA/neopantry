from rest_framework import permissions


class IsResourceOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check the URL.
        user_pk = view.kwargs.get('user_pk')
        if user_pk is not None:
            return int(user_pk) == request.user.pk

        # Check the request data.
        user = request.data.get('user')
        if user is not None:
            return int(user) == request.user.pk

        return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
