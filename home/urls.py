from . import views
from django.urls import path

app_name = "home"

urlpatterns = [
    path("home/",views.HomeView.as_view(),name="home"),
    path("postdetail/<int:post_id>/<slug:slug_id>/",views.PostDetailView.as_view(),name="postdetail"),
    path("profile/<int:user_id>/",views.ProfileUserView.as_view(),name="profile"),
    path("create/",views.PostCreateView.as_view(),name="create"),
    path("update/<int:post_id>/",views.PostUpdateView.as_view(),name="update"),
    path("delete/<int:post_id>/",views.PostDeleteView.as_view(),name="delete"),
    path("reply/<int:post_id>/<int:comment_id>/",views.CommentReplyView.as_view(),name="add_reply")
    
    
]