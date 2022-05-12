from .views import *

from django.urls import path

urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('create-test/', CreateTest.as_view(), name='create-test'),
    path('create-test/<int:test_pk>/', RedactTest.as_view(), name='redact-test'),
    path('test/<int:test_pk>/', GetTest.as_view(), name='test-page'),
    path('test/<int:test_pk>/completed/', TestResult.as_view(), name='completed-test-page'),
    path('test/', SearchTests.as_view(), name='search-test'),
    path('profile/', ShowProfile.as_view(), name='profile'),
]