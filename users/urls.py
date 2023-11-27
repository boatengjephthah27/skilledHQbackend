from django.urls import path, include
from rest_framework import routers
from . import views
from django.http import FileResponse, HttpResponseBadRequest


router = routers.DefaultRouter()
router.register(r'users', views.CustomUserViewSet)
router.register(r'organization', views.OrganizationViewSet)
router.register(r'address', views.AddressViewSet)
router.register(r'talent', views.TalentViewSet)
router.register(r'degree', views.DegreeViewSet)
router.register(r'project', views.ProjectViewSet)
router.register(r'technologies', views.TechnologiesUsedViewSet)
router.register(r'manager', views.ManagerViewSet)
router.register(r'skillstack', views.SkillStackViewSet)
router.register(r'language', views.LanguageViewSet)
router.register(r'socials', views.SocialViewSet)
router.register(r'experience', views.ExperienceViewSet)
router.register(r'challenge', views.ChallengeViewSet)
router.register(r'identityfiles', views.IdentityFilesViewSet)


def download_file(request):
    file_path = request.GET.get('file_path')

    if not file_path:
        return HttpResponseBadRequest("Missing 'file_path' parameter")

    response = FileResponse(open(file_path, 'rb'))
    return response


urlpatterns = [
    path('', include(router.urls),),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', views.LoginView.as_view(),  name='login'),
    path('logout/', views.LogoutView.as_view(),  name='logout'),
    path('download/', download_file, name='download'),
    path('talent-user/', views.TalentUserViewSet.as_view(),
         name='talent-user'),
    path('manager-user/', views.GetManagerViewSet.as_view(),
         name='manager-user'),
]
