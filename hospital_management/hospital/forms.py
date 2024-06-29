from django import forms
from .models import Appointment,Contact


class DateInput(forms.DateInput):
    input_type = 'date'


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

        widgets = {
            'Booking_date': DateInput(),
        }
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your message'}),
        }


from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [
            'doctor', 'patient_name', 'medication',
            'dosage', 'frequency', 'start_date',
            'end_date', 'notes'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


from django import forms
from .models import MedicalRecord

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient_name', 'diagnosis', 'treatment_plan', 'doctor']

class NurseSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)

class NurseLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput)



from django import forms
from .models import Pharmacist

class PharmacistSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Pharmacist
        fields = ['username', 'password']

class PharmacistLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

from django import forms
from .models import Bill, Patient

class BillForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=Patient.objects.all())
    date_issued = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    charge_descriptions = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}), required=False)
    charge_amounts = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}), required=False)

# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=100)
#     password = forms.CharField(widget=forms.PasswordInput)
#
# class SignUpForm(forms.ModelForm):
#     class Meta:
#         model = Patient
#         fields = ['first_name', 'last_name','date_of_birth','phone_number','email_id','password1','password2']
