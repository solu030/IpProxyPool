
# from django.views import View
# from rest_framework.generics import GenericAPIView
# from rest_framework.mixins import ListModelMixin, DestroyModelMixin, CreateModelMixin
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from app01.models import IpModel
from rest_framework.serializers import ModelSerializer
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from app01 import models


# Create your views here.
class IpSerializer(ModelSerializer):
    class Meta:
        model = models.IpModel
        fields = '__all__'
class IpView(generics.ListAPIView):
    filter_backends = [OrderingFilter]
    ordering_fields = ['score']     #?ordering=score
    queryset = models.IpModel.objects.all()
    serializer_class = IpSerializer

    def get(self, request):
        return self.list(request)

    # def post(self, request):
    #     return self.create(request)
    #
    # def delete(self, request):
    #     return self.destroy(request)
    # def destroy(self, request, *args, **kwargs):
    #     queryset = IpModel.objects.all()
    #     self.perform_destroy(queryset)
    #     return Response({"datail":"All Clear!"})