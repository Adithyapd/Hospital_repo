from django.contrib import admin

from . models import Department,Doctor,Patient
from . models import Appointment,Contact,Prescription,MedicalRecord,Bill
# Register your models here.
admin.site.register(Department)
admin.site.register(Doctor)
admin.site.register(Prescription)
admin.site.register(MedicalRecord)
admin.site.register(Patient)
admin.site.register(Bill)


class AppointmentAdmin(admin.ModelAdmin):
    list_display=('Patient_name','Phone_number','Email_id','Doctor_name','Booking_date','Booked_on','status')
    list_filter = ('status', 'Doctor_name', 'Booking_date')
    search_fields = ('Patient_name', 'Doctor_name', 'Email_id')


admin.site.register(Appointment, AppointmentAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display=('name','email','message','created_at')


admin.site.register(Contact,ContactAdmin)