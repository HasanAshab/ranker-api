from http import HTTPMethod
from rest_framework import permissions


class DeleteUserPermission(permissions.BasePermission):
    message = "You can't delete this user."

    def has_object_permission(self, request, view, obj):
        if request.method == HTTPMethod.DELETE:
            return self.can_delete_user(request.user, obj)
        return True

    def can_delete_user(self, user, target_user):
        return (
            user == target_user
            or (
                user.is_staff
                and not target_user.is_staff
                and not target_user.is_superuser
            )
            or (user.is_superuser and not target_user.is_superuser)
        )
