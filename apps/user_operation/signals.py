from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# 当这个User(UserProfile)model保存后调用
from .models import UserFav

# 接受post_save这种类型的信号量，接受USer的
@receiver(post_save, sender=UserFav)
def create_userfav(sender, instance=None, created=False, **kwargs):
	""" 添加收藏的时候"""
	if created:
		goods = instance.goods
		goods.fav_num += 1
		goods.save()


@receiver(post_delete, sender=UserFav)
def delete_userfav(sender, instance=None, created=False, **kwargs):
	"""当添加商品收藏时候"""
	goods = instance.goods
	goods.fav_num -= 1
	goods.save()


