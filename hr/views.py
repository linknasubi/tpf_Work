from django.http import HttpResponse
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
import datefinder
from datetime import datetime
import csv


from .models import CadEmpresa, CadServico, CadVeiculo, TbRastreioParada

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
    
    cad_empresa = []
    cad_servico = []
    cad_veiculo = []
    tb_rastreio_chamada_list = []

    
    #Instantiating the future query objects
    
    
    cad_empresa = CadEmpresa.objects.all()
    cad_empresa = sorted(cad_empresa.values_list("nome", flat=True))
    
    #Declaring the objects upon the referred model, and transforming it to a list
    #cad_empresa object is created before request so that can be initialized before the first request comes
    
    if request.method == "POST":
        
        form_empresa = [request.POST.get("empresa_cad")]
        form_servico = [request.POST.get("servico_cad")]
        form_veiculo = [request.POST.get("veiculo_cad")]
        form_parada_chamada = [request.POST.get("parada_chamada_tb")]
        
        
    #Assigning variable to the get form request objects, even that returns none

    if request.method == "POST" and form_empresa != None: 
        
        if form_empresa == ["Todos"]:
            form_empresa = cad_empresa
        
    
        id_cad_empresa = CadEmpresa.objects.all().filter(nome__in=form_empresa)
        id_cad_empresa = id_cad_empresa.values_list("id", flat=True)
        


        cad_servico = CadServico.objects.all().filter(cad_empresa_id__in = id_cad_empresa)
        cad_servico = sorted(cad_servico.values_list("nome", flat=True))
        
    
    #Assigning id from cad_empresa and creating cad_servico query object so that its id can be used in the following form
    
    
    if request.method == "POST" and form_servico != None:

        if form_servico == ["Todos"]:
            form_servico = cad_servico
        
        id_cad_servico = CadServico.objects.all().filter(nome__in=form_servico)
        id_cad_servico = id_cad_servico.values_list("id", flat=True)
        

        cad_veiculo = CadVeiculo.objects.all().filter(cad_servico_id__in = id_cad_servico) 
        cad_veiculo = sorted(cad_veiculo.values_list("nome", flat=True))
        
    #Assigning id from cad_servico and creating cad_veiculo query object so that its value can be used in the following form     

    
    if request.method == "POST" and form_veiculo != None:
        

        if form_veiculo == ["Todos"]:
            form_veiculo = cad_veiculo      

        tb_rastreio_parada = TbRastreioParada.objects.all()
        
        
        tb_rastreio_chamada = tb_rastreio_parada.filter(placa__in = form_veiculo)
        tb_rastreio_chamada_list = tb_rastreio_chamada.values_list("chamada", flat=True).distinct()
        
        

    if request.method == "POST" and form_parada_chamada != None:
        
        if form_parada_chamada == "Todos":
            form_parada_chamada = tb_rastreio_chamada_list 
        
        tb_rastreio_parada_date = tb_rastreio_chamada.filter(chamada__in = form_parada_chamada)
        
        
        homePage.tb_rastreio_parada_date = tb_rastreio_parada_date
        
    #Declaring the options "todos" so all fields can be selected, and declaring the attribute "tb_rastrei..." to be used in the csvExport  
    
    return render(request, 'hr/person_form.html', {"cad_empresa":cad_empresa, "cad_servico":cad_servico, "cad_veiculo":cad_veiculo,
                                                   "tb_rastreio_parada_chamada":tb_rastreio_chamada_list})


    

def csvExport(request):
    
    tb_rastreio_parada_date = homePage.tb_rastreio_parada_date
    
    
    form_parada_hour_start = request.POST.get("parada_hour_tb_start")
    form_parada_date_start = request.POST.get("parada_date_tb_start")
    form_parada_hour_end = request.POST.get("parada_hour_tb_end")
    form_parada_date_end = request.POST.get("parada_date_tb_end")
    
    gen_tb_rastreio = []

    """
    
        In the section below is created three arrays, each one responsible for a part of data filter. Due to limitations on the database
        such as the date time field not being in stamp model, but separated into days and hours, some complications came on the filtering,
        because of that, is created the following architecture. The array that ends with "start" gets all values referred to the first day selected,
        and filter the hour only inside it, after that, the same is did to the array that ends with "end", but to the last day selected, and finally
        the last array (that stays in the middle) are all the values between these days selected. After assigning values to these arrays is created
        a bufffer array that will transport these arrays so another one can transform all of three arrays into a single one.
    
    """



    if form_parada_date_start == form_parada_date_end:
        tb_rastreio_parada_hour_start = tb_rastreio_parada_date.filter(data = form_parada_date_start, hora__gte = form_parada_hour_start)
        tb_rastreio_parada_hour_end = tb_rastreio_parada_date.filter(data = form_parada_date_end, hora__lte = form_parada_hour_end)
        tb_rastreio_parada_hour_start = list(tb_rastreio_parada_hour_start.values_list())
        tb_rastreio_parada_hour_end = list(tb_rastreio_parada_hour_end.values_list())
        gen_tb_rastreio.append(tb_rastreio_parada_hour_start)
        gen_tb_rastreio.append(tb_rastreio_parada_hour_end)
        
        flat_list = [item for sublist in gen_tb_rastreio for item in sublist]
        
    else:
        tb_rastreio_parada_hour_start = tb_rastreio_parada_date.filter(data = form_parada_date_start, hora__gte = form_parada_hour_start)
        tb_rastreio_parada_hour_end = tb_rastreio_parada_date.filter(data = form_parada_date_end, hora__lte = form_parada_hour_end)
        tb_rastreio_parada_hour = tb_rastreio_parada_date.filter(data__range = [form_parada_date_start[0:8]+str(int(form_parada_date_start[8:])+1), form_parada_date_end[0:8]+str(int(form_parada_date_end[8:])-1)])
        tb_rastreio_parada_hour = list(tb_rastreio_parada_hour.values_list())
        tb_rastreio_parada_hour_start = list(tb_rastreio_parada_hour_start.values_list())
        tb_rastreio_parada_hour_end = list(tb_rastreio_parada_hour_end.values_list())
        gen_tb_rastreio.append(tb_rastreio_parada_hour_start)
        gen_tb_rastreio.append(tb_rastreio_parada_hour)
        gen_tb_rastreio.append(tb_rastreio_parada_hour_end)

        flat_list = [item for sublist in gen_tb_rastreio for item in sublist]

    """
        In the section below is created the response that will send the data directly to the url defined, "/download/".
        Also, the csv rows are formatted so it can be printed.
    
    """



    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(["placa","data","hora","segundos","longitude","latitude","lote", "servico", "chamada"])
    for i in range(len(flat_list)):
        value = flat_list[i]


        writer.writerow([value[1],value[2].strftime("%d/%m/%y"),
                         value[3].strftime("%H:%M:%S"),"null",value[5],value[6],value[7],value[8],value[9]])
    response['Content-Disposition'] = 'attachment; filename="tb_rastreio_parada.csv"'
    
    print(writer)
    
    return response
    
    
    








