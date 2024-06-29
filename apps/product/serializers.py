from rest_framework import serializers
from apps.product.models import (
                                 Category,
                                 SubCategory,
                                 Brand,
                                 Product
                                )


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class SubCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['name']


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'category', 
                  'sub_category', 'brand', 'unit', 'sku', 
                  'minimum_quantity', 'quantity', 
                  'description', 'tax', 'discount', 'price', 
                  'status', 'product_image', 'seller']