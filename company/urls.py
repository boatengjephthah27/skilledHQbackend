from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()

router.register(r'contracts', views.ContractViewsets)
router.register(r'applications', views.TalentApplicationViewsets)
router.register(r'role', views.RoleDescriptionViewsets)
router.register(r'role-responsibilities', views.ResponsibilityViewsets)
router.register(r'role-qualifications', views.QualificationViewsets)
router.register(r'billings', views.BillingViewsets)
router.register(r'contractchangerequest', views.ContractChangeRequestView)
router.register(r'suggested-contracts', views.SuggestedContractViews)


urlpatterns = [
    path('', include(router.urls)),
    path('messages/', views.MessageListCreateView.as_view(), name='message-list'),
    path('messages/<int:pk>/', views. MessageDetailView.as_view(),
         name='message-detail'),
    path('messages/<int:pk>/mark-as-read/',
         views.MarkMessageAsReadView.as_view(), name='mark-message-as-read'),
    path('contract-user/', views.ContractListViewsets.as_view(),
         name='contract-user'),
    path('suggested-talent/', views.SuggestedContractViewsets.as_view(),
         name='contract-user'),

]
