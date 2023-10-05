from rest_framework import routers

from schedule.views import LessonViewSet

router = routers.DefaultRouter()
router.register('lessons', LessonViewSet)

urlpatterns = router.urls