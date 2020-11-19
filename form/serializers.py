from .models import *
from rest_framework import serializers
from common.serializers import AttachmentSerializer

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields=['id','first_name','last_name','email','username']


class FormSerializer(serializers.ModelSerializer):
	creator_details=UserSerializer(read_only=True,source="created_by")
	collaborator_details=UserSerializer(read_only=True,many=True,source="collaborators")
	attachment_details=AttachmentSerializer(read_only=True,many=True,source="attachments")

	class Meta:
		model=Form
		fields='__all__'


class QuestionSerializer(serializers.ModelSerializer):
	attachment_details=AttachmentSerializer(read_only=True,many=True,source="attachments")

	class Meta:
		model=Question
		fields='__all__'


class OptionSerializer(serializers.ModelSerializer):
	attachment_details=AttachmentSerializer(read_only=True,many=True,source="attachments")
	
	class Meta:
		model=Option
		fields='__all__'


class QuestionDetailSerializer(serializers.ModelSerializer):
	attachment_details=AttachmentSerializer(read_only=True,many=True,source="attachments")
	option_details=OptionSerializer(read_only=True,many=True,source="options")

	class Meta:
		model=Question
		fields='__all__'


class FormDetailSerializer(serializers.ModelSerializer):
	creator_details=UserSerializer(read_only=True,source="created_by")
	collaborator_details=UserSerializer(read_only=True,many=True,source="collaborators")
	question_details=QuestionDetailSerializer(read_only=True,many=True,source="questions")
	attachment_details=AttachmentSerializer(read_only=True,many=True,source="attachments")

	class Meta:
		model=Form
		fields='__all__'

class QuestionAnswerSerializer(serializers.ModelSerializer):
	form_details=FormSerializer(read_only=True,source="form")
	question_details=QuestionDetailSerializer(read_only=True,source="question")
	answer_details=OptionSerializer(read_only=True,source="answer")

	class Meta:
		model=QuestionAnswer
		fields='__all__'

class ResponseSerializer(serializers.ModelSerializer):
	form_details=FormSerializer(read_only=True,source="form")
	user_details=UserSerializer(read_only=True,source="response_by")
	question_details=QuestionSerializer(read_only=True,many=True, source="questions")
	answer_details = QuestionAnswerSerializer(read_only=True,many=True, source="question_answers")

	class Meta:
		model=Response
		fields='__all__'