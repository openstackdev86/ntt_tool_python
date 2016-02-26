from django.conf.urls import patterns, url
from views import IndexView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
]