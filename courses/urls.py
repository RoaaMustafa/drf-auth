from django.urls import path
from .views import CourseList, CourseDetail

urlpatterns = [
    path('', CourseList.as_view(), name='Course_list'),
    path('<int:pk>/', CourseDetail.as_view(), name='Course_detail'),
]