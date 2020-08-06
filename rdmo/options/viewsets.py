from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rdmo.core.exports import XMLResponse
from rdmo.core.permissions import HasModelPermission

from .models import Option, OptionSet
from .renderers import OptionRenderer, OptionSetRenderer
from .serializers.export import (OptionExportSerializer,
                                 OptionSetExportSerializer)
from .serializers.v1 import (OptionIndexSerializer, OptionSerializer,
                             OptionSetIndexSerializer,
                             OptionSetNestedSerializer, OptionSetSerializer)


class OptionSetViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = OptionSet.objects.order_by('order')
    serializer_class = OptionSetSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'key',
        'comment'
    )

    @action(detail=False)
    def nested(self, request):
        serializer = OptionSetNestedSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        serializer = OptionSetIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=False, permission_classes=[HasModelPermission])
    def export(self, request):
        serializer = OptionSetExportSerializer(self.get_queryset(), many=True)
        xml = OptionSetRenderer().render(serializer.data)
        return XMLResponse(xml, name='optionsets.xml')

    @action(detail=True, url_path='export', permission_classes=[HasModelPermission])
    def detail_export(self, request, pk=None):
        optionset = self.get_object()
        serializer = OptionSetExportSerializer(optionset)
        xml = OptionSetRenderer().render([serializer.data])
        return XMLResponse(xml, name='{}.xml'.format(optionset.key))


class OptionViewSet(ModelViewSet):
    permission_classes = (HasModelPermission, )
    queryset = Option.objects.order_by('optionset__order', 'order')
    serializer_class = OptionSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'uri',
        'key',
        'optionset',
        'comment'
    )

    @action(detail=False)
    def index(self, request):
        serializer = OptionIndexSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(detail=False, permission_classes=[HasModelPermission])
    def export(self, request):
        serializer = OptionExportSerializer(self.get_queryset(), many=True)
        xml = OptionRenderer().render(serializer.data)
        return XMLResponse(xml, name='optionsets.xml')

    @action(detail=True, url_path='export', permission_classes=[HasModelPermission])
    def detail_export(self, request, pk=None):
        option = self.get_object()
        serializer = OptionExportSerializer(option)
        xml = OptionRenderer().render([serializer.data])
        return XMLResponse(xml, name='{}.xml'.format(option.key))
