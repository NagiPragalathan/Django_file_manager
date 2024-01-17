# Django  inbuilt models
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from QuizApp import settings

# Django views
from base.views.auth import *
from base.views.common import *
from base.views.FileManagement import *
from base.views.UserView import *
from base.views.QuestionManager import *

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

question_manager = [
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('add_question/<str:path>', add_question, name='add_question'),
    path('add_para_question/<str:path>', add_para_question, name='add_para_question'),
    path('edit_question/<str:path>', edit_question, name='edit_question'),
    path('para_edit_question/<str:path>/<str:cat>', para_edit_question, name='para_edit_question'),
    path('update_db', update_db, name='update_db'),
    path('add_image_editor', add_image_editor, name='add_image_editor'),
    path('update_para_db', update_para_db, name='update_para_db'),
    path('handle_questions', handle_questions, name='handle_questions'),
    path('handle_para_questions', handle_para_questions, name='handle_para_questions'),
    path('import_questions', import_questions, name='import_questions'),
    path('get_questions/<str:category>/', get_questions_by_category, name='get_questions_by_category'),
    path('delete_qust', delete_question, name='delete_question'),
    # Add other URL patterns if needed
]

UserView = [
    path('list_course/<str:path>', ListCourse, name='list_course'),
    path('take_quiz/<str:path>', take_quiz, name='take_quiz'),
    
]

urlpatterns.extend(admin_)
urlpatterns.extend(auth)
urlpatterns.extend(common)
urlpatterns.extend(file_manager)
urlpatterns.extend(question_manager)
urlpatterns.extend(UserView)

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
