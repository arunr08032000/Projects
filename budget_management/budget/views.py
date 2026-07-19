from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse


# Create your views here.
def index(request):
    budget_title = "Monthly Budget Management System"
    return render(request,"index.html", {'budget_title': budget_title})
