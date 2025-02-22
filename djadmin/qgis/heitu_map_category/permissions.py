from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限只允许对象的创建者才能编辑它。"""

    def has_object_permission(self, request, view, obj):
        # 读取权限被允许用于任何请求，
        # 所以我们始终允许 GET，HEAD 或 OPTIONS 请求。
        if request.method in permissions.SAFE_METHODS:
            return True
        # 写入权限只允许给 article 的作者。
        return obj.user == request.user
