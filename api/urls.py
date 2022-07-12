from django.urls import path
from django.conf.urls import url
from api import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register(r'shared', views.Link, basename='shared')
router.register(r'details', views.LinkDetails, basename='details')

urlpatterns = [
    path('files/', views.DocumentView.as_view(), name='files'),
    url(r'^download/(?P<filename>[-\w_\\-\\.]+)$', views.SomeFileDownloadView.as_view(), name='download'),
    path('multiple/', views.BaseFileDownloadViewMultiple.as_view(),name="multiple"),
    path('register/', views.RegisterApi.as_view()),
]

urlpatterns = urlpatterns + router.urls