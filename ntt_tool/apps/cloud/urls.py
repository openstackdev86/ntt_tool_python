from django.conf.urls import url
from rest_framework import routers
from views import *

router = routers.SimpleRouter()
router.register(r'cloud', CloudViewSet)
router.register(r'cloudtraffic', CloudTrafficViewSet)

urlpatterns = [
    url('^cloudtraffics/(?P<cloud>.+)/$', CloudTrafficListView.as_view()),

    # url('^cloudtraffic/$', CloudTrafficCreateView.as_view()),
    # url('^cloudtraffic/(?P<pk>[^/.]+)/$', CloudTrafficRetrieveView.as_view()),
    # url('^cloudtraffic/(?P<pk>[^/.]+)/$', CloudTrafficUpdateView.as_view()),
    # url('^cloudtraffic/(?P<pk>[^/.]+)/$', CloudTrafficDestroyView.as_view()),

    url('^cloudtraffictenants/(?P<cloud_traffic>.+)/$', CloudTrafficTenantsListView.as_view()),
    url('^cloudtraffictenant/$', CloudTrafficTenantsCreateView.as_view()),
    url('^cloudtraffictenant/(?P<pk>\d+)/$', CloudTrafficTenantsRetrieveView.as_view()),
    url('^cloudtraffictenant/(?P<pk>\d+)/$', CloudTrafficTenantsUpdateView.as_view()),
    url('^cloudtraffictenant/(?P<pk>\d+)/$', CloudTrafficTenantsDestroyView.as_view()),
]
urlpatterns += router.urls
