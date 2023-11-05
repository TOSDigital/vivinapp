from django import forms
from django.contrib.auth import get_user_model
from .models import *
from django.forms import formset_factory
from django_measurement.forms import MeasurementField
from measurement.measures import Area

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
        super().__init__(*args, **kwargs)
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
        super().__init__(*args, **kwargs)
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








  