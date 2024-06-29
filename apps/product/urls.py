from django.urls import path
from apps.product.views import (
                                 CategoryViews,
                                 CategoryRetrieveUpdateDestroyAPIViews,
                                 SubCategoryViews, 
                                 SubCategoryRetrieveUpdateDestroyAPIViews,
                                 BrandViews, BrandRetrieveUpdateDestroyAPIViews,
                                 ProductAPIView,
                                 ProductRetrieveUpdateDestroyAPIView
                                )


urlpatterns = [
    path("", ProductAPIView.as_view(), name="products"),
    path('<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-details'),
    path('category/', CategoryViews.as_view(), name="category"),
    path('category/<int:pk>/', CategoryRetrieveUpdateDestroyAPIViews.as_view(), name="category_details"),
    path('subcategory/', SubCategoryViews.as_view(), name="sub_category"),
    path('subcategory/<int:pk>/', SubCategoryRetrieveUpdateDestroyAPIViews.as_view(), name="sub_category_details"),
    path('brand/', BrandViews.as_view(), name="brand"),
    path('brand/<int:pk>/', BrandRetrieveUpdateDestroyAPIViews.as_view(), name='brand_details')
]
