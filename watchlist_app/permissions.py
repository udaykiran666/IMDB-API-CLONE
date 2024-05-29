    
#     admin_permission = super().has_permission(request, view)
# The super() function in Python is used to call a method from a parent class. In the context of your AdminOrReadOnly class, which extends permissions.IsAdminUser, the super() function is used to invoke the has_permission method from the IsAdminUser class.

# What Does super() Do Here?
# In your AdminOrReadOnly class, super().has_permission(request, view) calls the has_permission method of the parent class, IsAdminUser. This method checks if the user making the request is an admin user

from rest_framework import permissions

class AdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)

    # def has_permission(self, request, view):
    #     admin_permission = bool(request.user and request.user.is_staff)
    #     return request.method == "GET" or admin_permission # we need request.method == "GET" cause if that is not given we get issue like no permission


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `review_user` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.review_user == request.user