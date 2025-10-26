from django.contrib import admin
from django.urls import path
from strawberry.django.views import GraphQLView

from src.interface.graphql.schema import schema
from src.interface.rest.views import UploadView, DownloadView, ExportCSVView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql", GraphQLView.as_view(schema=schema)),
    path("api/upload", UploadView.as_view()),
    path("api/download/<str:file_id>", DownloadView.as_view()),
    path("api/export.csv", ExportCSVView.as_view()),
]