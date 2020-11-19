from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r'users', UserViewSet,  basename="users")
router.register(r'forms', FormViewSet, basename="forms")
router.register(r'questions', QuestionViewSet, basename="questions")
router.register(r'options', OptionViewSet, basename="options")
router.register(r'responses', ResponseViewSet, basename="options")

urlpatterns=[
    path('submit/',SubmitForm.as_view()),
    path('rest-auth/google/', GoogleLogin.as_view(), name='goggle_login'),
]


urlpatterns +=router.urls