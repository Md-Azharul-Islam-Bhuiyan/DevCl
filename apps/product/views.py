from django.shortcuts import render, get_object_or_404
from .filters import ProductFilter
from apps.product.models import (
                                  Category, SubCategory, Brand, Product
                                )
from apps.product.serializers import (
                                       CategorySerializers,
                                       SubCategorySerializers,
                                       BrandSerializers, 
                                       ProductSerializers
                                      )
from rest_framework.generics import (RetrieveUpdateDestroyAPIView, 
                                     ListCreateAPIView)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter


class CategoryViews(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class CategoryRetrieveUpdateDestroyAPIViews(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class SubCategoryViews(ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers


class SubCategoryRetrieveUpdateDestroyAPIViews(RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers


class BrandViews(ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers


class BrandRetrieveUpdateDestroyAPIViews(RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializers


class ProductAPIView(APIView):
    filterset_class = ProductFilter
    search_fields = ['product_name', 'summary', 'description']
    ordering_fields = ['price']

    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        
        # Filtering
        filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        serializer = ProductSerializers(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name', 'summary', 'description']
    ordering_fields = ['price']