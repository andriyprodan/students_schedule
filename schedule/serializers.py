from rest_framework import serializers

from schedule.models import Homework, Lesson


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'
        read_only_fields = ('id',)


class LessonSerializer(serializers.ModelSerializer):
    today_homework = serializers.SerializerMethodField()

    def get_today_homework(self, obj):
        if obj.today_homework_id:
            return HomeworkSerializer(Homework.objects.get(id=obj.today_homework_id)).data
        else:
            return None

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('id',)
