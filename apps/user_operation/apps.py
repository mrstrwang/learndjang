from django.apps import AppConfig


class UserOperationConfig(AppConfig):
    name = 'user_operation'
    verbose_name = '用户操作'

    # 信号量的注册
    def ready(self):
        import user_operation.signals