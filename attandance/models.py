from django.db import models
from datetime import date, datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django_measurement.models import MeasurementField
from measurement.measures import Area



# Create your models here.

class User(AbstractUser): 
    is_admin = models.BooleanField(default=False)
    is_office_login = models.BooleanField(default=False)
    is_site_engineer = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

def default_length():
    return Area(sq_ft=0)

class Project(models.Model):
    Project_name = models.CharField(max_length=300)
    Project_location = models.CharField(max_length=300)
    Project_Start_date = models.DateField()
    Project_End_date = models.DateField()
    Project_Dimensions = models.CharField(max_length=50)
    Floors = models.IntegerField()
    Builtup_area = models.CharField(max_length=100000)
    Length = MeasurementField(measurement=Area)
    Breadth = MeasurementField(measurement=Area)
    site_engineers = models.ManyToManyField('SiteEngineer', related_name='projects')
    

    def save(self, *args, **kwargs):
        if self.Length is None:  # Set default Length if it's not provided
            self.Length = Area(sq_ft=0)
        if self.Breadth is None:  # Set default Breadth if it's not provided
            self.Breadth = Area(sq_ft=0)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.Project_name

class OfficeLogin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    email = models.EmailField()
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class SiteEngineer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    email = models.EmailField()
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
class Contractor(models.Model):
    Contractor_name = models.CharField(max_length=500)
    Project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.Contractor_name} - {self.Project}"

class LaborTypes(models.Model):
    Contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING)
    Labor_type = models.CharField(max_length=500)
    wage = models.DecimalField(max_digits=10, decimal_places=2)
    overtime_wage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.overtime_wage:  # Check if overtime_wage is not manually set
            self.overtime_wage = self.calculate_overtime_wage()
        super(LaborTypes, self).save(*args, **kwargs)

    def calculate_overtime_wage(self):
        # Assuming overtime wage is wage divided by 8
        return self.wage / Decimal('8.0')



    def __str__(self):
        return f"{self.Contractor} - {self.Labor_type}"

class AttendanceRecord(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING)
    labor_type = models.ForeignKey(LaborTypes, on_delete=models.DO_NOTHING)
    date = models.DateField(auto_now_add=True)  # This will automatically set the current date when the record is created
    number_of_workers = models.PositiveIntegerField()
    Remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.project} - {self.contractor} - {self.labor_type} - {self.date}"

class OvertimeRecord(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    contractor = models.ForeignKey(Contractor, on_delete=models.DO_NOTHING)
    labor_type = models.ForeignKey(LaborTypes, on_delete=models.DO_NOTHING)
    date = models.DateField(auto_now_add=True)  # This will automatically set the current date when the record is created
    number_of_workers = models.PositiveIntegerField()
    number_of_hours = models.PositiveIntegerField()
    Remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.project} - {self.contractor} - {self.labor_type} - {self.date}"


class MaterialCategory(models.Model):
    CategoryName = models.CharField(max_length=300)

    def __str__(self):
        return self.CategoryName

class Material(models.Model):
    category = models.ForeignKey(MaterialCategory, on_delete=models.DO_NOTHING)
    Materialname = models.CharField(max_length=500)

    def __str__(self):
        return self.Materialname

class Indent(models.Model):
    date = models.DateField(auto_now_add=True)
    indent_no = models.IntegerField(null=True, blank=True)
    Project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    CategoryName = models.ForeignKey(MaterialCategory, on_delete=models.DO_NOTHING)
    Material = models.ForeignKey(Material, on_delete=models.DO_NOTHING)
    Quantity = models.DecimalField(decimal_places=2, max_digits=10, default="0")
    Quantity_order_status = models.BooleanField(default=False)
    Quantity_Recieved_status = models.BooleanField(default=False)

    def __str__(self):
        return self.indent_no


    


    



def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)

    


    