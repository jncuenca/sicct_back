from rest_framework import permissions

class IsContabilidadUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Contabilidad').exists()

class IsTesoreriaUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Tesoreria').exists()
    
class IsCallCenterUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='CallCenter').exists()
