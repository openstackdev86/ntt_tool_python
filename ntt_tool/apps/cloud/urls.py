from django.conf.urls import url
from rest_framework import routers
from views import *

router = routers.SimpleRouter()
router.register(r'cloud', CloudViewSet)
router.register(r'cloudtraffic', CloudTrafficViewSet)
router.register(r'cloudtraffictenant', CloudTrafficTenantsViewSet)

urlpatterns = [
    # url('^cloudtraffics/(?P<cloud>.+)/$', CloudTrafficListView.as_view()),
]
urlpatterns += router.urls
