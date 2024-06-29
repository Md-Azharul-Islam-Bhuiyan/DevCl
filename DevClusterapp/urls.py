from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth_user/', include('apps.account.urls')),
    path('api/v1/product/', include('apps.product.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Dev-Cluster Admin"
admin.site.site_title = "Dev-Cluster Admin Portal"
admin.site.index_title = "Welcome to the Dev-Cluster Portal"