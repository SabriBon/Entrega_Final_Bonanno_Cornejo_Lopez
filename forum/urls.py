from django.urls import path

from forum import views

app_name = "forum"
urlpatterns = [
    path("forum/", views.forum, name="forum-list"),
    path("forum/add", views.create_forum, name="forum-add"),
    path("forum/<int:pk>/detail/", views.ForumDetailView.as_view(), name="forum-detail"),
    path("forum/<int:pk>/update/", views.ForumUpdateView.as_view(), name="forum-update"),
    path("forum/<int:pk>/delete/", views.ForumDeleteView.as_view(), name="forum-delete"),
]
