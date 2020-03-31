from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
	# Had you added these fields from the start, there wouldn't be
	# a problem because the table has no existing rows?
	# However, if the table has already been created and you add a 
	# field that cannot be null, you have to define a default value to 
	# provide for any existing rows - otherwise, the database will not 
	# accept your changes because they would violate the data integrity constraints.
	creator = models.ForeignKey(User,on_delete=models.CASCADE)
	date    = models.DateField()
	name    = models.CharField(max_length=50)
	public  = models.BooleanField()
	limit_of_guests=models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.name


class Invitee(models.Model):
	name=models.ForeignKey(User,on_delete=models.CASCADE)
	event=models.ManyToManyField(Event,blank=True)

class Attendee(models.Model):
	name=models.ForeignKey(User,on_delete=models.CASCADE)
	event=models.ManyToManyField(Event,blank=True)

# Problem Statement
# Design and build a REST API for Event Registration

# Requirements
# Users can create events
# Users can limit the number of attendees
# Users can delete an event
# Users can view public events
# Private events can be viewed only by invited users
# Users should be able to register/unregister for an event
# Users cannot register for another event if its schedule overlaps with a previously registered event

# You'll have to submit the following:
# 1. REST API Documentation
# 2. Implementation of the API in Django Rest Framework