from django.shortcuts import render, reverse
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, TemplateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from attandance.models import SiteEngineer
from .forms import SiteUserModelForm
from django.core.mail import send_mail


# Create your views here.
class SiteUserListView(LoginRequiredMixin, ListView):
    template_name = "siteuserlist.html"
    
      # Set the model for the ListView

    def get_queryset(self):
        return SiteEngineer.objects.all()

class SiteUserCreateView(LoginRequiredMixin, CreateView):
    template_name = 'siteusercreate.html'
    form_class = SiteUserModelForm

    def get_success_url(self):
        return reverse("sitelogin:siteuserlistview")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_site_engineer = True
        user.is_office_login = False
        user.is_admin = False
        
        user.save()

        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']

        # Create a SalesLogin instance or any relevant model
        site_login = SiteEngineer.objects.create(
            user=user,
            name=name,
            email=email,
            phone=phone
        )
        # Send an email
        send_mail(
            subject="You are invited to be a office User",
            message="You were added as a Site User On Vivin Contracting and Engineering  LLP. Please Login to the website to start working",
            from_email="theonesolutionmysore@gmail.com",
            recipient_list=[user.email]
        )

        return super(SiteUserCreateView, self).form_valid(form)

# class OfficeUserUpdateView(LoginRequiredMixin, UpdateView):
#     template_name = 'officeuserupdate.html'
#     form_class = OfficeUserModelForm
    
#     def get_success_url(self):
#         return reverse("officeuser:officeuserlistview")

#     def get_queryset(self):
#         return OfficeLogin.objects.all()

# class SaleUserDeleteView(LoginRequiredMixin, DeleteView):
#     template_name = 'officeuserdelete.html'
#     context_object_name = 'officeuserdelete'
    
#     def get_success_url(self):
#         return reverse("officeuser:officeuserlistview")

#     def get_queryset(self):
#         return OfficeLogin.objects.all()from django.shortcuts import render

# Create your views here.
