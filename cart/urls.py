from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'order', views.OrderViewSet)
router.register(r'cart', views.CartViewSet)
router.register(r'skill', views.SkillViewSet)


urlpatterns = [
    path('', include(router.urls),),
]
