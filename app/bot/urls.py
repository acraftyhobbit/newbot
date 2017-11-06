from django.conf.urls import url

from .views import facebook, add_date, post_date, health_check

urlpatterns = [
    url('^facebook', facebook, name='Facebook'),
    url(r'^date', add_date, name='due_date'),
    url(r'^post_date', post_date, name='post_date'),
    url(r'healthcheck', health_check, name='health_check')
]
