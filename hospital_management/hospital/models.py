from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=25)
    image = models.ImageField(upload_to='media',blank=True,default='')

    def __str__(self):
        return '{}'.format(self.name)


class Doctor(models.Model):
    name = models.CharField(max_length=25)
    specialization = models.CharField(max_length=40)

    image = models.ImageField(upload_to='media', blank=True, default='')

    def __str__(self):
        return ' {}'.format(self.name) + ' ({})'.format(self.specialization)

class Appointment(models.Model):
    Patient_name = models.CharField(max_length=50)
    Phone_number = models.CharField(max_length=10)
    Email_id = models.EmailField()
    Doctor_name = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    Booking_date = models.DateField()
    Booked_on = models.DateField(auto_now=True)
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('rescheduled','rescheduled')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='')


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField(default='No message provided')
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.name)


class MedicalRecord(models.Model):
    patient_name = models.CharField(max_length=50)
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.patient_name)

class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor,null=True, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100,default='')
    medication = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField()


    def __str__(self):
        return '{}'.format(self.patient_name)

class Patient(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)





class Nurse(models.Model):

    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)

    # This should ideally be encrypted, but for simplicity, we're using CharField

    def __str__(self):
        return self.username

class Pharmacist(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username


from django.db import models

class Bill(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_issued = models.DateField()
    itemized_charges = models.JSONField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Bill for {self.patient.name} on {self.date_issued}"



