from django.contrib.auth.mixins import UserPassesTestMixin


class IsAdminUserMixin(UserPassesTestMixin):
    def test_func(self):
        self.request.user.is_authenticated and self.request.is_admin
        return super().test_func()