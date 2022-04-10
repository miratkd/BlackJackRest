from rest_framework import routers
from app1 import views

router = routers.DefaultRouter()
router.register(r'account', views.AccountViewSet)
router.register(r'math', views.MathViewSet)
urlpatterns = router.urls
