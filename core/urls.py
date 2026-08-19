from django.urls import path
from . import views

urlpatterns = [
    # HTML pages
    path('', views.index, name='index'),
    path('student/<str:name>/', views.student_dashboard, name='student_dashboard'),
    path('course/<str:title>/', views.course_detail, name='course_detail'),
    path('search/', views.search_courses, name='search_courses'),
    path('instructor/<str:name>/', views.instructor_courses, name='instructor_courses'),
    path('admin/seed/', views.admin_seed, name='admin_seed'),
    # API endpoints
    path('api/students/', views.api_students, name='api_students'),
    path('api/student/<str:name>/profile/', views.api_student_profile, name='api_student_profile'),
    path('api/student/<str:name>/courses/', views.api_student_courses, name='api_student_courses'),
    path('api/student/<str:name>/skills/', views.api_student_skills, name='api_student_skills'),
    path('api/student/<str:name>/recommendations/', views.api_student_recommendations, name='api_student_recommendations'),
    path('api/course/<str:title>/info/', views.api_course_info, name='api_course_info'),
    path('api/course/<str:title>/skills/', views.api_course_skills, name='api_course_skills'),
    path('api/course/<str:title>/prerequisites/', views.api_course_prerequisites, name='api_course_prerequisites'),
    path('api/course/<str:title>/instructors/', views.api_course_instructors, name='api_course_instructors'),
    path('health/', views.health, name='health'),
]