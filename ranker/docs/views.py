import os
from django.http import FileResponse
from django.conf import settings
from rest_framework.views import APIView


class SchemaView(APIView):
    def get(self, request, *args, **kwargs):
        schema_path = os.path.join(settings.SCHEMA_DIR, "schema.yml")
        return FileResponse(
            open(schema_path, "rb"), content_type="application/x-yaml"
        )
