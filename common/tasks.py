import random
from celery import shared_task
from common.models import *
from django.shortcuts import get_object_or_404

@shared_task(name="sum_two_numbers")
def add(x, y):
    return x + y

@shared_task(name="multiply_two_numbers")
def mul(x, y):
    total = x * (y * random.randint(3, 100))
    return total

@shared_task(name="sum_list_numbers")
def xsum(numbers):
    return sum(numbers)

@shared_task(name="copy")
def copy(id):
	modela_object = get_object_or_404(ModelA,id=id)
	ModelB.objects.create(title=modela_object.title,
							description=modela_object.description,
							created=modela_object.created,
							updated=modela_object.updated)
	modela_object.is_copied=True
	modela_object.save()
	return "is_copied = "+ str(modela_object.is_copied)


from django_celery_results.models import TaskResult
@shared_task(name="check_and_rerun")
def check_and_rerun(id):
	tasks = TaskResult.objects.filter(status='FAILURE').last()
	count = tasks.count()
	modela_object = get_object_or_404(ModelA,id=id)
	if count!=0:
		for retry in range(count):
			ModelB.objects.create(title=modela_object.title,
									description=modela_object.description,
									created=modela_object.created,
									updated=modela_object.updated)
		# tasks.delete()
		return "Failed tasks rerun complete"
	else:
		return "No failed tasks"