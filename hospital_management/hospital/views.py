from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse

from .models import Department,Doctor
from.forms import AppointmentForm
from django.contrib import messages
from .forms import ContactForm
# Create your views here.

def home(request):
    return render(request, 'home.html')
def about(request):
    return HttpResponse("About Page")


def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'confirmation.html')
    form = AppointmentForm()
    return render(request,'appointment.html',{'form':form})



def doctor(request):
    doctor = Doctor.objects.all()
    return render(request, 'doctor.html', {'doctor': doctor})


def patient(request):
    return render(request,'patient.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return render(request,'message.html')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def index(request):
    department=Department.objects.all()
    doctor=Doctor.objects.all()
    return render(request,'base.html',{'department':department,'doctor':doctor})



from .forms import PrescriptionForm


def create_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prescription_success')  # Redirect to a success page
    else:
        form = PrescriptionForm()

    return render(request, 'create_prescription.html', {'form': form})


def prescription_success(request):
    return render(request, 'prescription_success.html')


from .forms import MedicalRecordForm

def create_or_edit_medical_record(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')  # Redirect to the success page
    else:
        form = MedicalRecordForm()
    return render(request, 'medical_record_form.html', {'form': form})

def success_page(request):
    return render(request, 'success_page.html')






from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.hashers import check_password

def login_view(request):
    if request.method == "POST":
        name = request.POST['name']  # Change from 'email' to 'name'
        password = request.POST['password']
        try:
            patient = Patient.objects.get(name=name)  # Adjust to your model's field name
            if check_password(password, patient.password):
                request.session['patient_id'] = patient.id
                return redirect('patient_dashboard')
            else:
                return HttpResponse("Invalid credentials")
        except Patient.DoesNotExist:
            return HttpResponse("Invalid credentials")
    return render(request, 'login.html')

def signup_view(request):
    if request.method == "POST":
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            return render(request, 'signup.html', {'signup_error': 'Passwords do not match'})  # Update error key

        if Patient.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'signup_error': 'Email already exists'})  # Update error key

        patient = Patient(
            name=name,
            phone_number=phone_number,
            email=email,
            password=make_password(password)  # Hash the password before saving
        )
        patient.save()
        return redirect('login')
    return render(request, 'signup.html')




from .models import Appointment, Prescription, Patient, MedicalRecord

def patient_dashboard(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')

    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return redirect('login')

    # Adjust field names based on your model
    appointments = Appointment.objects.filter(Patient_name=patient.name)
    prescriptions = Prescription.objects.filter(patient_name=patient.name)

    context = {
        'patient': patient,
        'appointments': appointments,
        'prescriptions': prescriptions,
    }
    return render(request, 'patient_dashboard.html', context)


from .models import Patient

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    context = {
        'patient': patient
    }
    return render(request, 'patient_detail.html', context)


def cancel_appointment(request, appointment_id):
    if request.method == 'POST':
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.status = 'cancelled'
        appointment.save()
        return redirect('patient_dashboard')  # Redirect to the patient dashboard after canceling
    else:
        appointment = get_object_or_404(Appointment, id=appointment_id)
        return render(request, 'confirm_cancel_appointment.html', {'appointment': appointment})

def confirm_cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'confirm_cancel_appointment.html', {'appointment': appointment})


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment

def reschedule_appointment(request, appointment_id):
    if request.method == 'POST':
        new_date = request.POST.get('new_date')
        if new_date:
            appointment = get_object_or_404(Appointment, id=appointment_id)
            appointment.Booking_date = new_date
            appointment.status = 'rescheduled'
            appointment.save()
            return redirect('patient_dashboard')
    else:
        return render(request, 'reschedule_appointment.html', {'appointment_id': appointment_id})



def doctor_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        specialization = request.POST.get('specialization')
        password = request.POST.get('password')

        # Check if the provided name matches any existing doctor's name
        try:
            doctor = Doctor.objects.get(name=name)
            # Update the doctor's password
            user, created = User.objects.get_or_create(username=name)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password set successfully. You can now login.')
            # Redirect to the doctor login page
            return redirect('doctor_login')
        except Doctor.DoesNotExist:
            messages.error(request, 'No doctor found with the provided name.')
            return render(request, 'doctor_login.html')

    return render(request, 'doctor_login.html')


def doctor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            doctor = Doctor.objects.get(name=username)
            # Check if the provided username belongs to a doctor
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.username == username:
                    login(request, user)
                    messages.success(request, 'You have successfully logged in.')
                    return redirect(reverse('doctor_dashboard', kwargs={
                        'doctor_name': username}))  # Change to your doctor's dashboard view name
                else:
                    messages.error(request, 'You are not authorized to login here.')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        except Doctor.DoesNotExist:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'doctor_login.html')

def doctor_dashboard(request, doctor_name):
    try:
        # Retrieve the doctor object based on the name
        doctor = Doctor.objects.get(name=doctor_name)

        # Filter appointments and prescriptions based on the doctor
        appointments = Appointment.objects.filter(Doctor_name=doctor)
        prescriptions = Prescription.objects.filter(doctor=doctor)
        medical_records = MedicalRecord.objects.filter(doctor=doctor)

        # Render the dashboard with the filtered data
        return render(request, 'doctor_dashboard.html', {
            'doctor': doctor,
            'appointments': appointments,
            'prescriptions': prescriptions,
            'medical_records': medical_records
        })
    except Doctor.DoesNotExist:
        # Redirect to a login page or an error page if the doctor does not exist
        return redirect('doctor_login')


from .forms import NurseLoginForm, NurseSignupForm
from .models import Nurse

def nurse_register(request):
    if request.method == 'POST':
        form = NurseSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            Nurse.objects.create(username=username, password=password)
            messages.success(request, 'You have successfully registered.')
            return redirect('nurse_login')
    else:
        form = NurseSignupForm()
    return render(request, 'nurse_register.html', {'form': form})

def nurse_login(request):
    if request.method == 'POST':
        form = NurseLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                nurse = Nurse.objects.get(username=username, password=password)
                request.session['nurse_id'] = nurse.id
                messages.success(request, 'You have successfully logged in.')
                return redirect('nurse_dashboard')
            except Nurse.DoesNotExist:
                messages.error(request, 'Invalid username or password.')
    else:
        form = NurseLoginForm()
    return render(request, 'nurse_login.html', {'form': form})

def nurse_dashboard(request):
    nurse_id = request.session.get('nurse_id')
    if nurse_id:
        nurse = Nurse.objects.get(id=nurse_id)
        # Fetch all appointments and prescriptions (assuming they're not directly related to Nurse)
        appointments = Appointment.objects.all()
        prescriptions = Prescription.objects.all()
        return render(request, 'nurse_dashboard.html', {'nurse': nurse, 'appointments': appointments, 'prescriptions': prescriptions})
    else:
        return redirect('nurse_login')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from .forms import PharmacistSignupForm, PharmacistLoginForm, BillForm
from .models import Pharmacist, Bill, Appointment, Prescription, Patient

def pharmacist_register(request):
    if request.method == 'POST':
        form = PharmacistSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            hashed_password = make_password(password)
            try:
                Pharmacist.objects.create(username=username, password=hashed_password)
                messages.success(request, 'You have successfully registered.')
                return redirect('pharmacist_login')
            except IntegrityError:
                messages.error(request, 'Username already exists. Please choose another one.')
    else:
        form = PharmacistSignupForm()
    return render(request, 'pharmacist_register.html', {'form': form})

def pharmacist_login(request):
    if request.method == 'POST':
        form = PharmacistLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            pharmacists = Pharmacist.objects.filter(username=username)
            if pharmacists.exists():
                for pharmacist in pharmacists:
                    if check_password(password, pharmacist.password):
                        request.session['pharmacist_id'] = pharmacist.id
                        messages.success(request, 'You have successfully logged in.')
                        return redirect('pharmacist_dashboard')
                messages.error(request, 'Invalid username or password.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = PharmacistLoginForm()
    return render(request, 'pharmacist_login.html', {'form': form})

def pharmacist_dashboard(request):
    pharmacist_id = request.session.get('pharmacist_id')
    if pharmacist_id:
        pharmacist = Pharmacist.objects.get(id=pharmacist_id)
        appointments = Appointment.objects.all()
        prescriptions = Prescription.objects.all()
        bills = Bill.objects.all()
        return render(request, 'pharmacist_dashboard.html', {
            'pharmacist': pharmacist,
            'appointments': appointments,
            'prescriptions': prescriptions,
            'bills': bills
        })
    else:
        return redirect('pharmacist_login')

def create_bill(request):
    if request.method == 'POST':
        form = BillForm(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            date_issued = form.cleaned_data['date_issued']
            charge_descriptions = form.cleaned_data['charge_descriptions'].split('\n')
            charge_amounts = list(map(float, form.cleaned_data['charge_amounts'].split('\n')))
            itemized_charges = [{'description': desc, 'amount': amt} for desc, amt in zip(charge_descriptions, charge_amounts)]
            total_amount = sum(charge_amounts)
            Bill.objects.create(
                patient=patient,
                date_issued=date_issued,
                itemized_charges=itemized_charges,
                total_amount=total_amount
            )
            messages.success(request, 'Bill created successfully.')
            return redirect('pharmacist_dashboard')
    else:
        form = BillForm()
    return render(request, 'create_bill.html', {'form': form})

def view_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    return render(request, 'view_bill.html', {'bill': bill})




def signout(request):
    logout(request)
    return redirect('home')






