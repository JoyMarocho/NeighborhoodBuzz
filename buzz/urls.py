from django.urls import re_path as url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'register', views.register_user, name='register'),
    url(r'login', views.login_user, name='login'),
    url(r'logout', views.logout_user, name='logout'),
    url(r'profile/', views.profile, name='profile'),
    url(r'updateprofile', views.update_profile, name='updateprofile'),
    url('search/',views.search_results,name='search'),
    url('businesses/<int:neighborhood_id>/', views.businesses, name='businesses'),
    url('neighborhoods/', views.neighborhood, name='neighborhood'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)