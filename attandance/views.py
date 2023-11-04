from django.shortcuts import render, reverse
from .models import Project, User, UserProfile, OfficeLogin, SiteEngineer, AttendanceRecord, LaborTypes, Contractor
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, TemplateView, CreateView, View, FormView
from .forms import *
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.db.models import Sum, F, DecimalField, Q
from decimal import Decimal

# Create your views here.

# Proejct Views
class DashboardView(TemplateView):
    template_name = 'dashboard.html'

class ProjectListView(ListView):
    template_name = 'projects.html'
    queryset = Project.objects.all().order_by('-id')
    context_object_name = 'project'

class ProjectCreateView(CreateView):
    template_name = 'projectcreate.html'
    form_class = ProjectCreationForm

    def get_success_url(self):
        return reverse("projects")

class ProjectUpdateView(UpdateView):
    template_name = "projectupdate.html"
    model = Project
    form_class = ProjectCreationForm
    context_object_name = 'project'

    
    def get_success_url(self):
        return reverse("projects")

class ProjectDeatilView(DetailView):
    template_name = "projectdetail.html"
    model = Project
    context_object_name = 'projectdetail'


# project Views End 

# Attandance Feature start
class AttendanceRecordCreateView(CreateView):
    model = AttendanceRecord
    form_class = AttendanceRecordForm
    template_name = 'attendance_record.html'
    
    def get_success_url(self):
        return reverse("attendance_recordlist")


def load_contractors(request):
    project_id = request.GET.get('project')
    if project_id:  # Check if project_id is not None or empty string
        contractors = Contractor.objects.filter(Project_id=project_id).order_by('Contractor_name')
    else:
        contractors = Contractor.objects.none()
    return render(request, 'partials/contractor_dropdown_list_options.html', {'contractors': contractors})

def load_labor_types(request):
    contractor_id = request.GET.get('contractor')
    labor_types = LaborTypes.objects.filter(Contractor_id=contractor_id).order_by('Labor_type')
    return render(request, 'partials/labor_type_dropdown_list_options.html', {'labor_types': labor_types})

class AttendanceRecordListView(ListView):
    model = AttendanceRecord
    template_name = "attendance_record_list.html"
    context_object_name = 'recordlist'

class AttendanceRecordUpdateView(UpdateView):
    template_name = "attendance_record_list_update.html"
    model = AttendanceRecord
    context_object_name = 'attendance'
    fields = (
        'number_of_workers',
    )

    def get_success_url(self):
        return reverse("attendance_recordlist")

class AttendanceRecordDeleteView(DeleteView):
    model = AttendanceRecord
    context_object_name = 'attendancerecord'
    template_name = "attendance_record_delete.html"

    def get_success_url(self):
        return reverse("attendance_recordlist")


# Attandance Views End 

# Attandance report View 
class WageCalculationView(FormView):
    form_class = WageCalculationForm
    template_name = 'laborreport.html'

    def form_valid(self, form):
        project = form.cleaned_data['project']
        contractor = form.cleaned_data['contractor']
        from_date = form.cleaned_data['from_date']
        to_date = form.cleaned_data['to_date']

        # Fetch labor types for the contractor
        labor_types = LaborTypes.objects.filter(Contractor=contractor)
        # ...
        labor_types_with_wages = []

        for labor_type in labor_types:
            attendance_records = AttendanceRecord.objects.filter(
                project=project,
                contractor=contractor,
                labor_type=labor_type,
                date__range=(from_date, to_date)
            )
            total_workers = attendance_records.aggregate(
                total_workers=Sum('number_of_workers')
            )['total_workers'] or 0
            row_total = labor_type.wage * total_workers
            labor_types_with_wages.append({
                'labor_type': labor_type,
                'wage': labor_type.wage,
                'total_workers': total_workers,
                'row_total': row_total
            })

        total_wage = sum(ltw['row_total'] for ltw in labor_types_with_wages)

        # Check if the request is to download the excel
        if 'download_excel' in self.request.POST:
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            response['Content-Disposition'] = 'attachment; filename={date}-wage-report.xlsx'.format(
                date=timezone.now().strftime('%Y-%m-%d'),
            )
            wb = Workbook()
            ws = wb.active
            ws.title = 'Wage Report'

            # Write table headers
            columns = ['Labor Type', 'Wage per Worker', 'Number of Workers', 'Row Total']
            for col_num, column_title in enumerate(columns, start=1):
                ws.cell(row=1, column=col_num).value = column_title

            # Write table rows
            for row_num, ltw in enumerate(labor_types_with_wages, start=2):
                ws.cell(row=row_num, column=1).value = ltw['labor_type'].Labor_type
                ws.cell(row=row_num, column=2).value = ltw['wage']
                ws.cell(row=row_num, column=3).value = ltw['total_workers']
                ws.cell(row=row_num, column=4).value = ltw['row_total']

            # Write the total wage
            total_row_num = row_num + 1
            ws.cell(row=total_row_num, column=3).value = 'Total'
            ws.cell(row=total_row_num, column=4).value = total_wage

            # Add project and contractor details after the table
            details_start_row = total_row_num + 2
            ws.cell(row=details_start_row, column=1).value = 'Project Name:'
            ws.cell(row=details_start_row, column=2).value = project.Project_name

            ws.cell(row=details_start_row + 1, column=1).value = 'Contractor Name:'
            ws.cell(row=details_start_row + 1, column=2).value = contractor.Contractor_name

            ws.cell(row=details_start_row + 2, column=1).value = 'From Date:'
            ws.cell(row=details_start_row + 2, column=2).value = str(from_date)

            ws.cell(row=details_start_row + 3, column=1).value = 'To Date:'
            ws.cell(row=details_start_row + 3, column=2).value = str(to_date)

            wb.save(response)
            return response

        context = self.get_context_data(
            form=form,
            labor_types_with_wages=labor_types_with_wages,
            total_wage=total_wage,
            project=project,
            contractor=contractor,
            from_date=from_date,
            to_date=to_date
        )
        

        
        return self.render_to_response(context)

# Add this view to handle the AJAX request for the contractor dropdown
class ContractorOptionsView(View):
    def get(self, request, *args, **kwargs):
        project_id = request.GET.get('project')
        contractors = Contractor.objects.filter(Project_id=project_id)
        return JsonResponse(list(contractors.values('id', 'Contractor_name')), safe=False)


# Attandance report View end


 
    



