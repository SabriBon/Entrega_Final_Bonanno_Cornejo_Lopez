from django.urls import path

from accommodation import views

app_name = "accommodation"
urlpatterns = [
    path("accommodations/", views.AccommodationListView.as_view(), name="accommodation-list"),
    path("accommodation/add/", views.AccommodationCreateView.as_view(), name="accommodation-add"),
    path("accommodation/<int:pk>/detail/", views.AccommodationDetailView.as_view(), name="accommodation-detail"),
    path("accommodation/<int:pk>/update/", views.AccommodationUpdateView.as_view(), name="accommodation-update"),
    path("accommodation/<int:pk>/delete/", views.AccommodationDeleteView.as_view(), name="accommodation-delete"),
    path("comment/<int:pk>/add/", views.CommentCreateView.as_view(), name="comment-create"),
    path("comment/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
]

