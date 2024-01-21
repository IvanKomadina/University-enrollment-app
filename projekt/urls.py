"""
URL configuration for projekt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('adminHome/', views.adminHome, name='adminHome'),
    path('courses/', views.courses, name='courses'),
    path('addCourse/', views.addCourse, name='add_course'),
    path('editCourse/<int:courseID>', views.editCourse, name='edit_course'),
    path('students/', views.students, name='students'),
    path('addStudent/', views.addStudent, name='add_student'),
    path('editStudent/<int:studentID>', views.editStudent, name='edit_student'),
    path('profesors/', views.profesors, name='profesors'),
    path('addProfesor/', views.addProfesor, name='add_profesor'),
    path('editProfesor/<int:profesorID>', views.editProfesor, name='edit_profesor'),
    path('upisniList/<int:studentID>', views.upisniList, name='upisni_list'),
    path('studentsOnCourse/<int:courseID>', views.studentsOnCourse, name='students_on_course'),
    path('studentHome/', views.studentHome, name='studentHome'),
    path('profesorHome/', views.profesorHome, name='profesorHome'),
    path('profesorCourses/', views.profesorCourses, name='profesor_courses'),
    path('studentsOnCourseProfesor/<int:courseID>', views.studentsOnCourseProfesor, name='students_on_course_profesor'),
    path('filterPredmeta/<int:studentID>', views.filterPredmeta, name='filter_predmeta'),
    path('osobnaStatistika/<int:studentID>', views.osobnaStatistika, name='osobna_statistika'),
]
