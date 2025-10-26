from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ...core.ports import FileStoragePort

# Временный простой DI-хук; полноценный контейнер будет в src/di
FILE_STORAGE: FileStoragePort | None = None


class UploadView(APIView):
    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "file is required"}, status=status.HTTP_400_BAD_REQUEST)
        if FILE_STORAGE is None:
            return Response({"error": "storage not initialized"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        file_id = FILE_STORAGE.put_file(file.name, file.read())
        return Response({"file_id": file_id})


class DownloadView(APIView):
    def get(self, request, file_id: str):
        if FILE_STORAGE is None:
            return Response({"error": "storage not initialized"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        content = FILE_STORAGE.get_file(file_id)
        return Response(content, content_type="application/octet-stream")


class ExportCSVView(APIView):
    def get(self, request):
        # Заглушка: вернём пустой CSV
        return Response("candidate_id,score\n", content_type="text/csv")