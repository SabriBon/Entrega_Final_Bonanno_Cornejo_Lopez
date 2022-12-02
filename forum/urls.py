from django.urls import path

from forum import views

app_name = "forum"
urlpatterns = [
    path("forums/", views.ForumListView.as_view(), name="forum-list"),
    path("forum/add/", views.ForumCreateView.as_view(), name="forum-add"),
    path("forum/<int:pk>/detail/", views.ForumDetailView.as_view(), name="forum-detail"),
    path("forum/<int:pk>/update/", views.ForumUpdateView.as_view(), name="forum-update"),
    path("forum/<int:pk>/delete/", views.ForumDeleteView.as_view(), name="forum-delete"),
]
