from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# todo add UniversityBuilding model
# todo add Student model
# todo продумать логіку для викладачів, що заміняють предмет

class Room(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = 'Кабінет'
        verbose_name_plural = 'Кабінети'


# class Group(models.Model):
#     name = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Група'
#         verbose_name_plural = 'Групи'


class ScheduleCell(models.Model):
    day_of_week = models.PositiveSmallIntegerField(validators=[MaxValueValidator(6), MinValueValidator(0)])
    lesson_number = models.PositiveSmallIntegerField(validators=[MaxValueValidator(8), MinValueValidator(1)])
    schedule_number = models.PositiveSmallIntegerField(validators=[MaxValueValidator(2), MinValueValidator(1)])

    def __str__(self):
        return f'{self.schedule_number} {self.day_of_week} {self.lesson_number}'

    class Meta:
        verbose_name = 'Місце в розкладі'
        verbose_name_plural = 'Місце в розкладі'
        unique_together = ('day_of_week', 'lesson_number', 'schedule_number')


class Lesson(models.Model):
    schedule_cell = models.ForeignKey(ScheduleCell, on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)


class Subject(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE)
    # group = models.ForeignKey(Group, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    schedule_cells = models.ManyToManyField(ScheduleCell, through=Lesson)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предмети'


class Homework(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    text = models.TextField()
    deadline = models.DateField()

    def clean(self):
        if self.deadline.weekday() != self.lesson.schedule_cell.day_of_week:
            raise ValidationError('Дата не збігається з днем тижня')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Домашнє завдання'
        verbose_name_plural = 'Домашні завдання'
        unique_together = ('lesson', 'deadline')
