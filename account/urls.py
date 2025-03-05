from . import views
from django.urls import path

app_name = "account"

urlpatterns = [
    path("login/",views.LoginUserView.as_view(),name="login"),
    path("register/",views.RegisterUserView.as_view(),name="register"),
    path("logout/",views.LogoutView.as_view(),name="logout"),
    path("follow/<int:user_id>/",views.FollowUserView.as_view(),name="follow"),
    path("unfollow/<int:user_id>/",views.UnfollowUserView.as_view(),name="unfollow"),
    path("edit_user/",views.EditUserView.as_view(),name="edit_user"),
]