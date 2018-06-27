from .models import UserAddress,UserFav,UserLeavingMessage
import xadmin


class UserAddressAdmin(object):
	list_display = ["signer_name", "signer_mobile", "district", "address"]

class UserFavAdmin(object):
	pass

class UserLeavingMessageAdmin(object):
	pass

xadmin.site.register(UserLeavingMessage,UserLeavingMessageAdmin)
xadmin.site.register(UserFav,UserFavAdmin)
xadmin.site.register(UserAddress,UserAddressAdmin)

