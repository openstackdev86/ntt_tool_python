from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from models import *
from serializers import *


class CloudViewSet(viewsets.ModelViewSet):
    queryset = Cloud.objects.all()
    serializer_class = CloudSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CloudTrafficListView(generics.ListAPIView):
    serializer_class = CloudTrafficListSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CloudTraffic.objects.filter(cloud_id=self.kwargs.get('cloud'))


class CloudTrafficViewSet(viewsets.ModelViewSet):
    queryset = CloudTraffic.objects.all()
    serializer_class = CloudTrafficSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        import pdb
        pdb.set_trace()
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# class CloudTrafficRetrieveView(generics.RetrieveAPIView):
#     queryset = CloudTraffic.objects.all()
#     serializer_class = CloudTrafficRetrieveSerializer
#     authentication_classes = (JSONWebTokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#
#
# class CloudTrafficCreateView(generics.CreateAPIView):
#     serializer_class = CloudTrafficSerializer
#     authentication_classes = (JSONWebTokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#
#
# class CloudTrafficUpdateView(generics.UpdateAPIView):
#     # queryset = CloudTraffic.objects.all()
#     serializer_class = CloudTrafficSerializer
#     authentication_classes = (JSONWebTokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#
#     def update(self, request, *args, **kwargs):
#         import pdb
#         pdb.set_trace()
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)
#
#
# class CloudTrafficDestroyView(generics.DestroyAPIView):
#     queryset = CloudTraffic.objects.all()
#     serializer_class = CloudTrafficSerializer
#     authentication_classes = (JSONWebTokenAuthentication,)
#     permission_classes = (IsAuthenticated,)


class CloudTrafficTenantsListView(generics.ListAPIView):
    serializer_class = CloudTrafficTenantSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CloudTrafficTenants.objects.filter(cloud_traffic_id=self.kwargs.get('cloud_traffic'))


class CloudTrafficTenantsCreateView(generics.CreateAPIView):
    serializer_class = CloudTrafficTenantSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        tenant = CloudTrafficTenants()
        tenant.cloud_traffic_id = request.data.get("cloud_traffic_id")
        tenant.tenant_name = request.data.get("tenant_name")
        tenant.ssh_gateway = request.data.get("ssh_gateway")
        tenant.creator = request.user
        tenant.save()

        serializer = CloudTrafficTenantSerializer(tenant)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CloudTrafficTenantsUpdateView(generics.UpdateAPIView):
    queryset = CloudTrafficTenants.objects.all()
    serializer_class = CloudTrafficTenantSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CloudTrafficTenantsDestroyView(generics.DestroyAPIView):
    queryset = CloudTrafficTenants.objects.all()
    serializer_class = CloudTrafficTenantSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CloudTrafficTenantsRetrieveView(generics.RetrieveAPIView):
    queryset = CloudTrafficTenants.objects.all()
    serializer_class = CloudTrafficTenantSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
