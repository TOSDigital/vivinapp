from django.shortcuts import render, reverse
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, TemplateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from attandance.models import OfficeLogin
from .forms import OfficeUserModelForm
from django.core.mail import send_mail


# Create your views here.
class OfficeUserListView(LoginRequiredMixin, ListView):
    template_name = "officeuserlist.html"
    
      # Set the model for the ListView

    def get_queryset(self):
        return OfficeLogin.objects.all()

class OfficeUserCreateView(LoginRequiredMixin, CreateView):
    template_name = 'officeusercreate.html'
    form_class = OfficeUserModelForm

    def get_success_url(self):
        return reverse("officeuser:officeuserlistview")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_office_login = True
        user.is_admin = False
        user.is_site_engineer = False
        user.save()

        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']

        # Create a SalesLogin instance or any relevant model
        office_login = OfficeLogin.objects.create(
            user=user,
            name=name,
            email=email,
            phone=phone
        )
        # Send an email
        send_mail(
            subject="You are invited to be a office User",
            message="You were added as a office User On Vivin Contracting and Engineering  LLP. Please Login to the website to start working",
            from_email="theonesolutionmysore@gmail.com",
            recipient_list=[user.email]
        )

        return super(OfficeUserCreateView, self).form_valid(form)

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
#         return OfficeLogin.objects.all()