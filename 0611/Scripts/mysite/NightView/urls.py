from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'$', view.index),
]


urlpatterns += staticfiles_urlpatterns()