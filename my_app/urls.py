from django.urls import path

from my_app import views

app_name = "my_app"
urlpatterns = [
    path("destinos/", views.DestinoListView.as_view(), name="destino-list"),
    path("destino/add", views.DestinoCreateView.as_view(), name="destino-add"),
    path("destino/<int:pk>/detail/", views.DestinoDetailView.as_view(), name="destino-detail"),
    path("destino/<int:pk>/update/", views.DestinoUpdateView.as_view(), name="destino-update"),
    path("destino/<int:pk>/delete/", views.DestinoDeleteView.as_view(), name="destino-delete"),

]
