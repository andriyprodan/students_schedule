from django.db import models
from django.db.models import OuterRef, Subquery, Value
from django.db.models.functions import Coalesce
from rest_framework import viewsets
from rest_framework.response import Response

from schedule.models import Homework, Lesson
from schedule.serializers import HomeworkSerializer, LessonSerializer


# Create your views here.
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.select_related('schedule_cell', 'subject').prefetch_related('homework_set').all()
    serializer_class = LessonSerializer

    # filterset_class = HomeworkFilterSet

    def list(self, request, *args, **kwargs):
        # Define a subquery to get the latest homework for each lesson
        latest_homework = Homework.objects.filter(
            lesson=OuterRef('pk'),
        ).order_by('-deadline')

        # Define a subquery to get the latest homework deadline for each lesson

        # Create a queryset for lessons with the latest homework deadlines
        # lessons_with_latest_homework = Lesson.objects.annotate(
        #     latest_homework_deadline=Subquery(latest_homework_deadline, output_field=models.DateField())
        # )

        # Define the date range for filtering homework
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Filter homework by the date range
        homework_filtered_by_date_range = Homework.objects.filter(
            deadline__range=(start_date, end_date),
            lesson=OuterRef('pk')
        )

        # Use Coalesce to get the latest homework or None if there's no homework in the date range
        lessons = Lesson.objects.annotate(
            today_homework_id=Coalesce(
                Subquery(homework_filtered_by_date_range.values('id')[:1]),
                Subquery(latest_homework.values('id')[:1]),
                Value(None),
                output_field=models.TextField()
            )
        ).all()
        serializer = self.get_serializer(lessons, many=True)
        return Response({'schedule': serializer.data})
