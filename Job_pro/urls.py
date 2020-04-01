"""Job_pro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from job_app import views

urlpatterns = [
    path('',views.index, name="index"),
    path('application_guide',views.application_guide,name='app_guide'),
    path('accounts/login/',views.user_login,name="login"),
    path('register/',views.register,name ='register'),
    path('my_jobpage/',views.get_userPage,name='application_details'),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('logout/',views.user_logout,name='logout'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('client_details/<int:user_id>',views.get_profile,name='userinfor'),
    path('EditEdu_details/<int:user_id>',views.UpdateEduInfo,name='editEduInfor'),
    path('EditEmp_details/<int:user_id>',views.UpdateEmploymentDetails,name='editEmpInfor'),
    path('EditUser_details/<int:user_id>',views.UpdateUserInfo,name='editUserInfor'),
    path('EditPrefernce_details/<int:user_id>',views.UpdatePreferenceDetails,name='editPrefInfor'),
    path('Editfile_uplaoded_details/<int:user_id>',views.Update_fileUploads,name='editFile_updateInfor'),
    path('Add_edu_info/<int:user_id>',views.add_eduInfo,name='add_eduInfo'),
    path('Add_user_info/<int:user_id>',views.add_userInfo,name='add_userInfo'),
    path('Add_emp_info/<int:user_id>',views.add_empInfo,name='add_empInfo'),
    path('Add_userpref_info/<int:user_id>',views.add_Prefinfo,name='add_Prefinfo'),
    path('Add_files/<int:user_id>',views.upload_file,name='upload_file'),
    path('admin/', admin.site.urls),
]
