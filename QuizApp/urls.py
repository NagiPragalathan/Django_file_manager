# Django  inbuilt models
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from QuizApp import settings

# Django views
from base.views.auth import *
from base.views.common import *
from base.views.FileManagement import *

urlpatterns = []

admin_ = [
    path('admin/', admin.site.urls),    
]

auth = [
    path('accounts/', include('django.contrib.auth.urls')),  # Use built-in authentication views
    path('enter_otp', enter_otp, name='enter_otp'),
    path('signup/<str:mail>', signup, name='signup'),
    path('login', user_login, name='login'),
]
common = [
    path('home', home, name='home'),
    path('', home, name='home'),
]

file_manager = [
    path('add_data', add_data, name='add_data'),
    path('list_data', list_data, name='list_data'),
    path('add_folder', add_folder, name='add_folder'),
    path('list_folders/<str:path>', list_folders, name='list_folders'),
]

urlpatterns.extend(auth)
urlpatterns.extend(common)
urlpatterns.extend(file_manager)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

