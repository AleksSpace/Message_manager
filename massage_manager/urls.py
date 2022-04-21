from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from massage_manager.yasg import swaggerurlpatterns
from servise_msg.views import ClientViewSet, MailingViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'mailings', MailingViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include("rest_framework.urls",
                              namespace="rest_framework"))
]

urlpatterns += swaggerurlpatterns
