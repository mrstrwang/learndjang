from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

	#从数据库取到的用户
	def has_object_permission(self, request, view, obj):
		#如果是get请求就可以，其他请求直接返回
		if request.method in permissions.SAFE_METHODS:
			return True
		# 判断是否是同一个用户
		return obj.user == request.user