"""
Views for the user API.
"""
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Student, StudentSubject, Subject

from django.db.models import Sum

from student.serializers import (
    CustomUserSerializer,
    AuthTokenSerializer,
    StudentSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new student in the system."""
    serializer_class = CustomUserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class RetrieveStudentPerformanceView(generics.RetrieveAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.student
    

@api_view(['GET'])
def get_highest_total_score(request):
    highest_scorer = Student.objects.annotate(total_marks=Sum('studentsubject__marks')).order_by('-total_marks').first()
    if highest_scorer:
        student_data = {
            'name': highest_scorer.user.name,
            'roll_number': highest_scorer.roll_number,
            'total_marks': highest_scorer.total_marks
        }
        return Response({'student': student_data})
    else:
        return Response({'message': 'No students found.'}, status=404)
    

@api_view(['GET'])
def get_highest_subject_scorers(request):
    subjects = Subject.objects.all()
    highest_scorers = []

    for subject in subjects:
        highest_scorer = StudentSubject.objects.filter(subject=subject).order_by('-marks').first()
        if highest_scorer:
            student = highest_scorer.student
            student_data = {
                'name': student.user.name,
                'roll_number': student.roll_number,
                'marks': highest_scorer.marks
            }
            highest_scorers.append({'subject': subject.name, 'student': student_data})

    return Response({'highest_scorers': highest_scorers})
