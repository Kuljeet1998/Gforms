from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)

admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Response)
admin.site.register(QuestionAnswer)

class FormAdmin(admin.ModelAdmin):
	fieldsets = [
			("General",			{'fields':['description']}),
			("User related",	{'fields':['created_by','collaborators']}),
			("Upload",			{'fields':['attachments']})
	]
	list_display = ('title', 'description', 'created_by')
	list_filter = ['title','created']
	search_fields = ['title']
	ordering = ['title']

admin.site.register(Form,FormAdmin)