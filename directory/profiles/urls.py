from django.urls import path 

from . import views


urlpatterns = [
    path("list/", views.TeacherListView.as_view(), name="teachers_list"),
    path("detail/<int:pk>/", views.TeacherDetailView.as_view(), name="teachers_detail"),
    path("create-bulk/", views.TeacherBulkCreateView.as_view(), name="teachers_create_bulk")
]