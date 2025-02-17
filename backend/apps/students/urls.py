from .views import StudentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'students', views.StudentViewSet)  # Vérifie bien que la classe StudentViewSet est bien dans views

urlpatterns = router.urls
