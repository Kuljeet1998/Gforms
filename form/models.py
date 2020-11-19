from django.db import models
from common.models import *
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class User(AbstractUser, UUIDTimeStamp):
	pass
	@property
	def full_name(self):
		return '{first_name} {last_name}'.format(first_name=self.first_name,last_name=self.last_name)

	def __str__(self):
		return self.full_name

class Form(UUIDTimeStamp, Enum):
	description = models.CharField(max_length=200)
	
	created_by = models.ForeignKey(User,
									related_name="forms",
									on_delete=models.CASCADE)
	collaborators = models.ManyToManyField(User,
											related_name="collaborator_in_forms",
											null=True,
											blank=True)
	attachments = models.ManyToManyField(Attachment,
										related_name="forms",
										blank=True,
										null=True)

	def __str__(self):
		return self.title


class Question(UUIDTimeStamp, Enum):
	is_required=models.BooleanField(default=False)

	form = models.ForeignKey(Form,
							related_name="questions",
							on_delete=models.CASCADE)
	attachments = models.ManyToManyField(Attachment,
										related_name="questions",
										blank=True,
										null=True)

	def __str__(self):
		return "{title} - ({form})".format(form=self.form.title,title=self.title)


class Option(UUIDTimeStamp, Enum):
	question = models.ForeignKey(Question,
								related_name="options",
								on_delete=models.CASCADE)
	
	attachments = models.ManyToManyField(Attachment,
										related_name="options",
										blank=True,
										null=True)

	def __str__(self):
		return "({form}) - ({question}) - {title} ".format(form=self.question.form.title,title=self.title,question=self.question.title)

	

class Response(UUIDTimeStamp):

	form = models.ForeignKey(Form,
							related_name="responses",
							on_delete=models.CASCADE)
	response_by = models.ForeignKey(User,
									related_name="responses",
									on_delete=models.CASCADE)
	questions = models.ManyToManyField(Question,
										through="QuestionAnswer",
										related_name="responses")


class QuestionAnswer(UUIDTimeStamp):

	question = models.ForeignKey(Question,
								related_name="question_answers",
								on_delete=models.CASCADE)
	response = models.ForeignKey(Response,
								related_name="question_answers",
								on_delete=models.CASCADE)
	answer = models.ForeignKey(Option,
								related_name="question_answers",
								on_delete=models.CASCADE,
								null=True,blank=True)