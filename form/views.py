from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response as RestResponse
from rest_framework import (exceptions)

#Google log-in
from google.oauth2 import id_token
from google.auth.transport import requests
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.google.provider import GoogleProvider


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):

	queryset=User.objects.all()
	serializer_class=UserSerializer
	http_method_names = ['get', 'put','post']


class FormViewSet(viewsets.ModelViewSet):
	filter_backends = [filters.SearchFilter]
	search_fields = ['title']

	queryset=Form.objects.all()

	def get_serializer_class(self):
		if self.action=='retrieve' or self.action=='update':
			return FormDetailSerializer
		return FormSerializer

	def create(self, request, *args, **kwargs):
		self.request.data['created_by'] = self.request.user.id
		return super().create(request, *args, **kwargs)

class QuestionViewSet(viewsets.ModelViewSet):
	filter_backends = [filters.SearchFilter]
	search_fields = ['title']

	queryset=Question.objects.all()

	def get_serializer_class(self):
		if self.action=='retrieve' or self.action=='update':
			return QuestionDetailSerializer
		return QuestionSerializer

class OptionViewSet(viewsets.ModelViewSet):
	filter_backends = [filters.SearchFilter]
	search_fields = ['title']

	queryset=Option.objects.all()
	serializer_class=OptionSerializer


class ResponseViewSet(viewsets.ModelViewSet):
	filter_backends = [filters.SearchFilter]
	search_fields = ['title']

	queryset=Response.objects.all()
	serializer_class=OptionSerializer


class SubmitForm(APIView):

	def post(self,request):
		form_id = request.data.get('form', None)
		user = request.user

		if not form_id:
			raise exceptions.ValidationError({"error": "key form is required!"})

		form_object = get_object_or_404(Form,
										id=form_id)

		question_answers = request.data.get('question_answer', None) #Array of dictionary containing all the question ids as "key" and answer marked for it as "value"
		if not question_answers:
			raise exceptions.ValidationError({"error": "key question_answers is required!"})

		response_object = Response.objects.create(form=form_object,
												response_by=user)

		for question_answer in question_answers:
			question_id = question_answer["question"]
			answer_id = question_answer["answer"]
			
			question_object = get_object_or_404(Question,
											id=question_id)
			answer_object = get_object_or_404(Option,
											id=answer_id)

			if str(question_object.form.id) != form_id:
				raise exceptions.ValidationError({"error": "Question ({q_id}) does not belong to this form ".format(q_id=question_id)})

			if str(answer_object.question.id) != question_id:
				raise exceptions.ValidationError({"error": "Answer ({a_id}) does not belong to this question ({q_id}) ".format(q_id=question_id,a_id=answer_id)})

			QuestionAnswer.objects.create(question=question_object,
											answer=answer_object,
											response=response_object)

		data = ResponseSerializer(response_object).data
		return RestResponse(data, status=200)

#Google Login (medium.com)
# class GoogleOAuth2AdapterIdToken(GoogleOAuth2Adapter):
# 	def complete_login(self, request, app, token, **kwargs):
# 		idinfo = id_token.verify_oauth2_token(token.token, requests.Request(), app.client_id)
# 		if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
# 			raise ValueError('Wrong issuer.')
# 		extra_data = idinfo
# 		login = self.get_provider().sociallogin_from_response(request,extra_data)
# 		return login
# oauth2_login = OAuth2LoginView.adapter_view(GoogleOAuth2AdapterIdToken)
# oauth2_callback = OAuth2CallbackView.adapter_view(GoogleOAuth2AdapterIdToken)


from rest_auth.registration.views import SocialLoginView, SocialConnectView 
from allauth.socialaccount.providers.oauth2.client import OAuth2Client


class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    basic_auth = False


class GoogleLogin(SocialLoginView):
    adapter_class = CustomGoogleOAuth2Adapter
    client_class = OAuth2Client


class GoogleConnect(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client