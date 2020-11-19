from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import post_save, pre_save
from .models import User
from django.dispatch import receiver
import sendgrid
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import http.client
from urllib.parse import urlencode
import requests
import json
@receiver(post_save,sender=User)
def send_mail_to_user(sender, instance, created,**kwargs):
	if created:
		sender_email = User.objects.get(username="admin").email
		# msg = send_mail('New Login',
		# 				'Welcome to trello board',
		# 				'kbhengura@gmail.com' , 
		# 				[instance.email], 
		# 				fail_silently=False)
		# message = Mail(
  #   					from_email='kbhengura@gmail.com',
  #   					to_emails=instance.email,
  #   					subject='New Login',
  #   					html_content='<strong>Welcome to trello board</strong>')

		# sg = SendGridAPIClient('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')
		# response = sg.send(message)
		# print(response.status_code, response.body, response.headers)
		
		
		conn = http.client.HTTPSConnection("api.sendgrid.com")

		data = {
  					"personalizations": [
				    {
				      "to": [
				        {
				          "email":instance.email
				        }
				      ],
				      "dynamic_template_data":{
				      		"firstname":instance.first_name,
				      		"lastname":instance.last_name,
				      		"username":instance.username
				      },
				      "subject": "Hello, World!"
				    }
				  ],
  					"from": {
				    "email": "kbhengura@gmail.com"
				  },
				  "template_id": "d-dcaf1ce92989485d8171f6aea09b6d4f",
				}



		headers = {
    				'authorization': "Bearer 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",
    				'content-type': "application/json"
    			}
		# import pdb;
		# pdb.set_trace()
		# conn.request("POST", "/v3/mail/send", urlencode(data), headers)
		# import pdb;
		# pdb.set_trace()
		# res = conn.getresponse()
		# data = res.read()
		# print(data.decode("utf-8"))
		url = "https://api.sendgrid.com/v3/mail/send"
		response = requests.request("POST", url, data=json.dumps(data), headers=headers)
		print(response.text)