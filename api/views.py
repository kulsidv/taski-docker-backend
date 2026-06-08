from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer
from .cache import cache


class TaskView(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()

    CACHE_KEY_LIST = "tasks:list"
    CACHE_KEY_DETAIL_PREFIX = "task:"

    def list(self, request, *args, **kwargs):
        if cache.exists(self.CACHE_KEY_LIST):
            cached_data = cache.get_data(self.CACHE_KEY_LIST)
            if cached_data is not None:
                return Response(cached_data)

        response = super().list(request, *args, **kwargs)
        cache.set_data(self.CACHE_KEY_LIST, response.data)
        return response

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        cache_key = f"{self.CACHE_KEY_DETAIL_PREFIX}{pk}"

        if cache.exists(cache_key):
            cached_data = cache.get_data(cache_key)
            if cached_data is not None:
                return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        cache.set_data(cache_key, response.data)
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self._invalidate_cache(instance)
        instance.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _invalidate_cache(self, instance=None):
        cache.delete_data(self.CACHE_KEY_LIST)
        if instance:
            cache.delete_data(f"{self.CACHE_KEY_DETAIL_PREFIX}{instance.pk}")

    def perform_create(self, serializer):
        instance = serializer.save()
        self._invalidate_cache(instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        self._invalidate_cache(instance)