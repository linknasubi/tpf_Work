from django.http import HttpResponse
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy

from .models import Person, Cad_servico, Cad_veiculo, TbRastreioParada
from .forms import PersonForm

def loginPage(request):
    #form = UserCreationForm()
    if request.user.is_authenticated:
        return redirect('person_changelist')
    else:
            
        if request.method == 'POST':
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('person_changelist')
            else:
                messages.info(request, "Username or password is incorrect")
            
        context = {}    
        return render(request, 'hr/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def homePage(request):
    return render(request, 'hr/person_form.html')


class PersonListView(ListView):
    model = Person
    context_object_name = 'people'


class PersonCreateView(CreateView):
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy('person_changelist')


class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonForm
    success_url = reverse_lazy('person_changelist')

def load_data(request):
    cad_veiculo_id = request.GET.get('cad_servico')  
    print(request.GET.get('cad_servico'))
    log_parada = TbRastreioParada.objects.filter(placa=cad_veiculo_id).order_by('nome')
    context = {'log_parada': log_parada}
    return render(request, 'hr/table.html', context)

def load_cities(request):
    cad_empresa_id = request.GET.get('cad_empresa')    
    cities = Cad_servico.objects.filter(cad_empresa_id=cad_empresa_id).order_by('nome')
    context = {'cities': cities}
    return render(request, 'hr/city_dropdown_list_options.html', context)

def load_vanues(request):
    cad_servico_id = request.GET.get('cad_servico')    
    vanues = Cad_veiculo.objects.filter(cad_servico_id=cad_servico_id).order_by('nome')
    context = {'vanues': vanues}
    return render(request, 'hr/vanue_ddl.html', context)














