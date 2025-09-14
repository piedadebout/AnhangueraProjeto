from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def gerencia(request):
    return render(request, "gerencia/gerencia.html")