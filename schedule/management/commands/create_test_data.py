from pprint import pprint
import datetime
import random

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.test import TestCase
from django.urls import reverse

from schedule.models import Room, Subject, ScheduleCell, Lesson, Homework
from students_schedule.test_utils import random_words, random_string, random_number
from teachers.models import Teacher

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        #         create users
        User.objects.bulk_create(
            User(
                username=f'{random_words()}' + '/' + random_string(3),
                email=f'{random_words()}@{random_words(1)}.com',
                first_name=random_words(),
                last_name=random_words(),
                phone=f'+380{random_number(length=9)}',
                role=User.Role.TEACHER
            )
            for i in range(10)
        )
        teacher_users = User.objects.filter(role=User.Role.TEACHER)
        #         create teachers
        Teacher.objects.bulk_create([
            Teacher(
                user=teacher_users[i]
            )
            for i in range(10)
        ])
        #         create rooms
        Room.objects.bulk_create([
            Room(
                number=random_number(),
            )
            for i in range(3)
        ])
    # create subjects
        Subject.objects.bulk_create([
            Subject(
                name=random_words(),
                teacher=random.choice(Teacher.objects.all()),
                room=random.choice(Room.objects.all())
            )
            for i in range(15)
        ])
        subjects = Subject.objects.all()
        schedule_cells = ScheduleCell.objects.all()
        #        create lessons
        Lesson.objects.bulk_create([
            Lesson(
                subject=random.choice(subjects),
                schedule_cell=cell
            )
            for cell in schedule_cells
        ])
        lessons = Lesson.objects.all()
        sometime = datetime.date.today() - datetime.timedelta(days=50)
        Homework.objects.bulk_create([
            Homework(
                lesson=random.choice(lessons),
                text=random_words(10),
                deadline=sometime + datetime.timedelta(days=i)
            )
            for i in range(60)
        ])
