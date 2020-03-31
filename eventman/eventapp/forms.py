from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Submit
from .models import Event,Invitee,Attendee
from bootstrap_datepicker_plus import DatePickerInput

class EventForm(forms.ModelForm):
	
	company_name = forms.CharField(
        label="Nombre de la Compañía",
        max_length=90,
        widget=forms.TextInput(),
        required=True,
    )

	class Meta:
		model  = Event
		fields = ['date','name','public','limit_of_guests']

		widgets = {
			'date' : DatePickerInput(),
			'creator': forms.TextInput(attrs={'disabled': True}),
		}

	


# {% if submitbutton == "Submit" %} 
# <h1>event name    :  {{form.name}}</h1>
# <h1>event date    :  {{form.date}}</h1>
# <h1>event public  :  {{form.public}}</h1>
# <h1>event creator :  {{form.creator}}</h1>

# <button onclick="window.location.href = '{% url 'profile' %}';">OK</button>

# {% endif %}
