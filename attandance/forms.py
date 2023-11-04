from django import forms
from django.contrib.auth import get_user_model
from .models import Project, User, UserProfile, OfficeLogin, SiteEngineer, AttendanceRecord, LaborTypes, Contractor
from django.forms import formset_factory
from django_measurement.forms import MeasurementField
from measurement.measures import Area

class ProjectCreationForm(forms.ModelForm):
    Length = MeasurementField(measurement=Area, unit_choices=[('sq_ft', 'Square Feet')])
    Breadth = MeasurementField(measurement=Area, unit_choices=[('sq_ft', 'Square Feet')])

    class Meta:
        model = Project
        fields = (
            'Project_name',
            'Project_location',
            'Project_Start_date',
            'Project_End_date',
            'Project_Dimensions',
            'Floors',
            'Builtup_area',
            'Length',
            'Breadth',



        )
        widgets = {
            'Project_Start_date': forms.DateInput(attrs={'type': 'date'}),
            'Project_End_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['project', 'contractor', 'labor_type', 'number_of_workers']

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









  