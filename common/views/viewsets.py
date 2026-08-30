from django.db.models import QuerySet
from rest_framework.viewsets import ModelViewSet
from common.responses.success import OkResponse, CreatedResponse
from common.query.query_mixin import QueryMixin
from common.serializers.serializers import SerializerActionMixin
from common.constants.messages import Messages
from common.pagination.page_number import StandardPagination
from typing import ClassVar
from common.constants.audit import AuditActionEnum
from apps.audit_logging.services import AuditLogService
from apps.audit_logging.models import Action

class BaseModelViewSet(
    SerializerActionMixin,
    QueryMixin,
    ModelViewSet,
):
    """
    Base ViewSet for all API resources.

    Provides:
    - Dynamic serializers per action
    - Query parameter handling
    - Selector integration
    - Standard API responses
    """


    selector: ClassVar = None

    pagination_class = StandardPagination

    def get_queryset(self) -> QuerySet:

        if self.selector:
            return self.selector.get_queryset()

        return super().get_queryset()


    def list(self, request, *args, **kwargs):
        
        queryset = self.filter_queryset(
            self.get_queryset()
        )

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(
                serializer.data
            )

        serializer = self.get_serializer(queryset, many=True)

        return OkResponse(
            data=serializer.data,
            message=Messages.RETRIEVED
        )


    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()

        serializer = self.get_serializer(instance)

        return OkResponse(
            data=serializer.data,
            message=Messages.RETRIEVED
        )


    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        AuditLogService.log(
            request=request,
            action=Action.CREATED,
            instance=serializer.instance,
        )

        return CreatedResponse(
            data=serializer.data,
            message=Messages.CREATED
        )


    def update(self, request, *args, **kwargs):

        partial = kwargs.pop(
            "partial",
            False
        )

        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )

        serializer.is_valid(raise_exception=True)

        original_data = AuditLogService.serialize_instance(instance)

        self.perform_update(serializer)

        instance.refresh_from_db()

        current_data = AuditLogService.serialize_instance(instance)

        changes = AuditLogService.diff(
            original_data,
            current_data
        )

        AuditLogService.log(
            audit_action=AuditActionEnum.UPDATE,
            request=request,
            action=Action.UPDATED,
            instance=instance,
            original=original_data,
            changes=changes,
        )

        return OkResponse(
            data=serializer.data,
            message=Messages.UPDATED
        )


    def partial_update(self, request, *args, **kwargs):

        kwargs["partial"] = True

        return self.update(
            request,
            *args,
            **kwargs
        )


    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()

        AuditLogService.log(
            audit_action=AuditActionEnum.DELETE,
            request=request,
            action=Action.DELETED,
            instance=instance,
        )

        self.perform_destroy(instance)

        return OkResponse(message=Messages.DELETED)