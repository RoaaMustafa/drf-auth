from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Course
from .serializers import CourseSerializer
from .permissions import IsOwnerOrReadOnly

class CourseList(ListCreateAPIView):
    """
    List all courses.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetail(RetrieveUpdateDestroyAPIView):
    """
    List a single course.
    """
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
