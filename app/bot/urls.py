from django.conf.urls import url

from .views import facebook, add_date, post_date, update_project, post_project, select_supply, post_supply

"""URL routing for views.py"""

urlpatterns = [
    url('^facebook', facebook, name='Facebook'),
    url(r'^date', add_date, name='due_date'),
    url(r'^post_date', post_date, name='post_date'),
    url(r'^project', update_project, name='update_project'),
    url(r'^post_project', post_project, name='post_date'),
    url(r'^pattern', select_supply, name='select_pattern'),
    url(r'^post_supply', post_supply, name='post_supply'),
    url(r'^material', select_supply, name='select_material')
]
