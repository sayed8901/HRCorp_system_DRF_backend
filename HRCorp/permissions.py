from rest_framework import permissions


class IsPowerUserForModifyButStandardOrPowerUserForPOST(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow any user to view the list if authenticated
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow both power_user and standard_user to create (POST)
        if request.method == 'POST' and request.user.is_authenticated and request.user.user_type in ['power_user', 'standard_user']:
            return True
        
        # Only allow power_user to update (PUT, PATCH) or delete (DELETE)
        if request.method in ['PUT', 'PATCH', 'DELETE'] and request.user.is_authenticated and request.user.user_type == 'power_user':
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Allow any user to view the object if authenticated
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only allow power_user to update (PUT, PATCH) or delete (DELETE)
        if request.user.is_authenticated and request.user.user_type == 'power_user':
            return True
        
        return False




class IsPowerOrStandardUserOtherwiseReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # all the viewer (if users are not authenticated) can view
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allowing both power_user and standard_user
        if request.user.is_authenticated and request.user.user_type in ['power_user', 'standard_user']:
            return True
        else:
            return False
    
    
    # N.B.: the below declared 'has_object_permission' function will only execute if the above created 'has_permission' function returns True

    def has_object_permission(self, request, view, obj):
        # providing read permission (GET, HEAD or options request)  by allowing SAFE_METHODS to all users
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # providing Write permission (PUT or PATCH) to both power_user and standard_user
            if request.user.user_type in ['power_user', 'standard_user']:
                return True
            else:
                return False
    