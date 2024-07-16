from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet


class ReadOnly(permissions.BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: ModelViewSet,
        obj: Model,
    ) -> bool:
        return request.method in permissions.SAFE_METHODS


class IsOwner(permissions.BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: ModelViewSet,
        obj: Model,
    ) -> bool:
        return obj.owner == request.user
