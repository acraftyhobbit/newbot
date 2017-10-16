from django.conf.urls import url

from .views import facebook

urlpatterns = [
    url('^facebook', facebook, name='Facebook')
]
