from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'userprofiles', views.UserProfileViewSet)
router.register(r'useraccounts', views.UserAccountViewSet)
router.register(r'permission', views.PermissionViewSet)
# changing base name fucks it up somehow, NOTE: investiogate further
router.register(r'contacts', views.ContactViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'home', views.HomeViewSet, 'home')
router.register(r'question', views.CustomQuestionViewSet)
router.register(r'answer', views.CustomAnswerViewSet)
#router.register(r'customcontact', views.CustomContactViewSet, 'customcontact')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/checkemail/', views.check_email),
    path('api-auth/changepassword/', views.change_password),
    path('api-auth/alt-login/', views.login),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('userprofiles/<int:id>/fields/', views.get_profile_fields)
]
