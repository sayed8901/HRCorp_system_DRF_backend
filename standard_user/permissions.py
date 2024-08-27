from rest_framework import permissions


# permission defined for standard user
class IsStandardUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # all the viewer (if users are not authenticated) can view
        if request.method in permissions.SAFE_METHODS:
            return True
        # also, the Authenticated users & standard_user only can see list view
        if request.user.is_authenticated and request.user.user_type == 'standard_user':
            return True
        else:
            return False
    
    
    # N.B.: the below declared 'has_object_permission' function will only execute if the above created 'has_permission' function returns True

    def has_object_permission(self, request, view, obj):
        # providing read permission (GET, HEAD or options request)  by allowing SAFE_METHODS to all users
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # providing Write permission (PUT or PATCH)  only to  the standard_user
            if request.user.user_type == 'standard_user':
                return True
            else:
                return False
    

    


# permission defined for standard_user type user
class IsStandardUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.user_type == 'standard_user':
            return True
        else:
            return False
        



