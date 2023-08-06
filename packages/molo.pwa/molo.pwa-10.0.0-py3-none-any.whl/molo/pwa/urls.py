from django.conf.urls import re_path

from fcm_django.api.rest_framework import FCMDeviceViewSet
from rest_framework.routers import DefaultRouter

from .views import RegistrationTokenView, manifest, service_worker, fcm, toast


urlpatterns = []

router = DefaultRouter()
router.register(r'devices', FCMDeviceViewSet)

urlpatterns += [
    re_path(
        r'^notification_devices/$', RegistrationTokenView.as_view(),
        name='registration-token'),
    re_path('^serviceworker.js$', service_worker),
    re_path('^manifest.json$', manifest),
    re_path('^fcm.js$', fcm),
    re_path('^toast.min.js$', toast),
]
