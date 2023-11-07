from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import *
from django.forms import formset_factory
from django_measurement.forms import MeasurementField
from measurement.measures import Area

User = get_user_model()

class CreateCustomUser(UserCreationForm):
    class Meta:
        model = User
        fields = {"username",}
        field_classes = {'username': UsernameField}

class ProjectCreationForm(forms.ModelForm):
    Length = MeasurementField(measurement=Area, unit_choices=[('sq_ft', 'Feet')])
    Breadth = MeasurementField(measurement=Area, unit_choices=[('sq_ft', 'Feet')])

    class Meta:
        model = Project
        fields = (
            'Project_name',
            'Project_location',
            'Project_Start_date',
            'Project_End_date',
            'Floors',
            'Builtup_area',
            'Length',
            'Breadth',
            'Project_Dimensions',
            'site_engineers',
        )
        widgets = {
            'Project_Start_date': forms.DateInput(attrs={'type': 'date'}),
            'Project_End_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['project', 'contractor', 'labor_type', 'number_of_workers', 'Remarks']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retrieve the user argument and remove it from kwargs
        super().__init__(*args, **kwargs)

        # If user is provided, filter the project's queryset based on the user's role
        if user is not None:
            if user.is_admin or user.is_office_login:
                self.fields['project'].queryset = Project.objects.all()
            elif user.is_site_engineer:
                self.fields['project'].queryset = user.siteengineer.projects.all()
            else:
                self.fields['project'].queryset = Project.objects.none()

        # The rest of your __init__ remains unchanged
        self.fields['contractor'].queryset = Contractor.objects.none()
        self.fields['labor_type'].queryset = LaborTypes.objects.none()

        if 'project' in self.data:
            try:
                project_id = int(self.data.get('project'))
                self.fields['contractor'].queryset = Contractor.objects.filter(Project_id=project_id).order_by('Contractor_name')
                if 'contractor' in self.data:
                    contractor_id = int(self.data.get('contractor'))
                    self.fields['labor_type'].queryset = LaborTypes.objects.filter(Contractor_id=contractor_id).order_by('Labor_type')
            except (ValueError, TypeError):
                pass  # In case of ValueError or TypeError, do not set any queryset
        elif self.instance.pk:
            self.fields['contractor'].queryset = self.instance.project.contractor_set.order_by('Contractor_name')
            self.fields['labor_type'].queryset = self.instance.contractor.labortypes_set.order_by('Labor_type')




class WageCalculationForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    contractor = forms.ModelChoiceField(queryset=Contractor.objects.none())  # Initially empty
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(WageCalculationForm, self).__init__(*args, **kwargs)
        if 'project' in self.data:
            try:
                project_id = int(self.data.get('project'))
                self.fields['contractor'].queryset = Contractor.objects.filter(Project_id=project_id).order_by('Contractor_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Contractor queryset

class OvertimeWageCalculationForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    contractor = forms.ModelChoiceField(queryset=Contractor.objects.none())  # Initially empty
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(OvertimeWageCalculationForm, self).__init__(*args, **kwargs)
        self.fields['contractor'].queryset = Contractor.objects.none()

        if 'project' in self.data:
            try:
                project_id = int(self.data.get('project'))
                self.fields['contractor'].queryset = Contractor.objects.filter(Project_id=project_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Contractor queryset

class ContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = (
            'Contractor_name',
            'Project'
        )

class LaborTypeForm(forms.ModelForm):
    class Meta:
        model = LaborTypes
        fields = ['Contractor', 'Labor_type', 'wage', 'overtime_wage']

class OvertimeRecordForm(forms.ModelForm):
    class Meta:
        model = OvertimeRecord
        fields = ['project', 'contractor', 'labor_type', 'number_of_workers', 'number_of_hours', 'Remarks']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user is not None:
            if user.is_admin or user.is_office_login:
                self.fields['project'].queryset = Project.objects.all()
            elif user.is_site_engineer:
                self.fields['project'].queryset = user.siteengineer.projects.all()
            else:
                self.fields['project'].queryset = Project.objects.none()



        self.fields['contractor'].queryset = Contractor.objects.none()
        self.fields['labor_type'].queryset = LaborTypes.objects.none()

        if 'project' in self.data:
            try:
                project_id = int(self.data.get('project'))
                self.fields['contractor'].queryset = Contractor.objects.filter(Project=project_id).order_by('Contractor_name')
                if 'contractor' in self.data:
                    contractor_id = int(self.data.get('contractor'))
                    self.fields['labor_type'].queryset = LaborTypes.objects.filter(Contractor=contractor_id).order_by('Labor_type')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['contractor'].queryset = self.instance.project.contractor_set.order_by('Contractor_name')
            self.fields['labor_type'].queryset = self.instance.contractor.labortypes_set.order_by('Labor_type')

class MaterialCategoryForm(forms.ModelForm):
    class Meta:
        model = MaterialCategory
        fields = (
            'CategoryName',
        )

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields= (
            'category',
            'Materialname',
        )

class IndentCreateForm(forms.ModelForm):
    class Meta:
        model = Indent
        fields = ['Project', 'indent_no','CategoryName', 'Material', 'Quantity']


class IndentUpdateForm(forms.ModelForm):
    class Meta:
        model = Indent
        fields = ['Quantity_order_status', 'Quantity_Recieved_status']

    






  