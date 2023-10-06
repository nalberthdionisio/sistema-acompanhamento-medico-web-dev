
from django.contrib import auth, messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.messages import constants
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.db.models.signals import post_save
from django.dispatch import receiver
from medical.forms2 import formcadProc, formSug, formUser,FormUserProcedure
from medical.models import Procedure, Recommendation, Users, UserProcedure, ProcedureReco
from django.utils import timezone
import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import date
from datetime import datetime, timedelta


# from django.http import HttpResponse
def cad(request):
    if request.method == "GET":
        return render(request, "medical/pages/cad.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        try:
            user = Users.objects.create_user(
                username=username, email=email, password=senha
            )
            user.save()
            return render(request, "medical/pages/home.html")
        except:
            return render(request, "medical/pages/cad.html")


def login(request):
    if request.method == "GET":
        return render(request, "medical/pages/login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        senha = request.POST.get("senha")

        user = auth.authenticate(username=username, password=senha)

        if not user:
            messages.add_message(
                request, constants.ERROR, "Username ou senha inválidos"
            )
            return redirect("/")
        else:
            auth.login(request, user)
            return redirect("/main")

def logout(request):
    auth.logout(request)
    return redirect("/")

@login_required(login_url='/')
def main(request):
    user = Users.objects.filter(is_superuser=False)
    today = date.today()
    
    usuarios_atrasados = UserProcedure.objects.filter(date_limit__lt = today)
    atrasos = []
    for users in usuarios_atrasados:
        if users.user not in atrasos:
            atrasos.append(users.user)
    # print(atrasos)
    
    usuarios_aptos = UserProcedure.objects.all()
    aptos = []
    for users1 in usuarios_aptos:

        if users1.done == True:
            if users1.user not in aptos:
                aptos.append(users1.user)
        else: 
            if users1.user in aptos:
                aptos.remove(users1.user)
    print(aptos)

    usuarios_atualizados = UserProcedure.objects.filter(done=True).order_by('-id')
    atualizados = []
    for users2 in usuarios_atualizados:
        if users2.user not in atualizados:
            atualizados.append(users2.user)
    # print(atualizados)
    # usuarios_atrasados = Users.objects.filter(userprocedure__date_limit__lt=today)
    # pacientes_aptos = Users.objects.exclude(userprocedure__isnull=True).exclude(userprocedure__done=False)
    # pacientes_atualizados = Users.objects.filter(userprocedure__done=True).order_by('-userprocedure__date_done')
    # qnt_aptos = Users.objects.exclude(userprocedure__isnull=True).exclude(userprocedure__done=False).count()
    # qnt_atrasados = Users.objects.filter(userprocedure__date_limit__lt=today).count()
    # qnt_atualizados = Users.objects.filter(userprocedure__done=True).order_by('-userprocedure__date_done').count()
    # {'qnt_atualizados':qnt_atualizados,'qnt_atrasados':qnt_atrasados,'qnt_aptos':qnt_aptos,'user':user,'usuarios_atrasados':usuarios_atrasados, 'pacientes_aptos':pacientes_aptos,'pacientes_atualizados':pacientes_atualizados}

    
    return render(request, 'medical/pages/main.html', {'user':user,'atrasos':atrasos,'atualizados':atualizados,'aptos':aptos,
                                                       'atualizadosc':len(atualizados),
                                                       'atrasosc':len(atrasos),
                                                       'aptosc':len(aptos),
                                                       })

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProcedure

@receiver(post_save, sender=UserProcedure)
def update_date_limit(sender, instance, **kwargs):
    user_procedure = instance

    if user_procedure.done and user_procedure.date_limit is not None:
        user_procedure.date_limit = None
        user_procedure.save(update_fields=['date_limit'])

@login_required(login_url='/')
def show_finalization_patient(request):
    user = Users.objects.filter(is_superuser=False)
    qtnduser = Users.objects.filter(is_superuser = False).count()
    return render(request, 'medical/pages/show_finalization_patient.html',{'user':user})

# def cadrec(request):
#     pat = Users.objects.filter(is_superuser=False)
#     return render(request, 'medical/pages/cadrec.html', {'pat': pat})


# crud proc
@login_required(login_url='/')
def find_all_procedure(request):

    user = Users.objects.filter(is_superuser=False)
    procreco = ProcedureReco.objects.all()
    proc = Procedure.objects.filter()
    search = request.GET.get('search')
    if search:
        proc = proc.filter(title__icontains=search)
    paginator = Paginator(proc, 10)
    page = request.GET.get('page')
    proc = paginator.get_page(page)

    return render(request, 'medical/pages/show_procedure.html', {'proc': proc, 'user': user, 'procreco': procreco})


@login_required(login_url='/')
def create_procedure(request):
    form = formcadProc(request.POST)
    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('show_procedure')
    else:
        form = formcadProc()
    return render(request, 'medical/pages/procedure.html', {'formproc': form})


@receiver(post_save, sender=UserProcedure)
def atualizar_data(sender, instance, **kwargs):
    if instance.done:
        new_date = timezone.now()
        UserProcedure.objects.filter(pk=instance.pk).update(date_done=new_date)

@login_required(login_url='/')
def update_procedure(request, id):
    proc = Procedure.objects.get(id=id)
    form = formcadProc(instance=proc)

    if request.method == 'POST':
        form = formcadProc(request.POST, instance=proc)
        if form.is_valid():
            form.save()
            return redirect('show_procedure')
    return render(request, 'medical/pages/update_procedure.html', {'formproc': form})

@login_required(login_url='/')
def delete_procedure(request, id):
    proc = get_object_or_404(Procedure, pk=id)
    proc.delete()
    return redirect("show_procedure")


# crud recommedation
@login_required(login_url='/')
def find_all_recommendation(request):
    reco = Recommendation.objects.all()
    search = request.GET.get('search')
    if search:
        reco = reco.filter(name__icontains=search)
    
    paginator = Paginator(reco,10)
    page = request.GET.get('page')
    reco = paginator.get_page(page)
    return render(request, 'medical/pages/show_recommendation.html', {'reco': reco})

@login_required(login_url='/')
def create_recommendation(request):
    form = formSug(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('show_recommendation')
    return render(request, 'medical/pages/recommendation.html', {'formreco': form})

@login_required(login_url='/')
def update_recommendation(request, id):
    reco = Recommendation.objects.get(id=id)
    form = formSug(instance=reco)

    if request.method == 'POST':
        form = formSug(request.POST, instance=reco)
        if form.is_valid():
            form.save()
            return redirect('show_recommendation')
    return render(request, 'medical/pages/update_recommendation.html', {'formreco': form})

@login_required(login_url='/')
def delete_recommendation(request, id):
    reco = get_object_or_404(Recommendation, pk=id)
    reco.delete()
    return redirect("show_recommendation")

    # for user in users:
    #     print(f"Paciente: {user.username}")

    #     procedimentos_pre = user.userprocedure_set.filter(type_procedure='pre_op')
    #     for pre_op in procedimentos_pre:
    #         print(f"Procedimento pré-operatório: {pre_op.procedure.title}")

    #     procedimentos_pos = user.userprocedure_set.filter(type_procedure='pos_op')
    #     for pos_op in procedimentos_pos:
    #         print(f"Procedimento pós-operatório: {pos_op.procedure.title}")
    # user_id_to_filter = 94
    
    # user = users.filter(id=user_id_to_filter).first()
    # if user:
    #     print(f"User: {user.username}")
    #     pre_op_procedures = user.procedures.filter(type_procedure=True)
    #     for procedure in pre_op_procedures:
    #         print(f"  Pre-op Procedure: {procedure.procedure.title}")

@login_required(login_url='/')
def find_all_patient(request):
    users = Users.objects.filter(is_superuser=False).order_by('-id')
    userprocedure = UserProcedure.objects.all()

    search = request.GET.get('search')
    if search:
        users = users.filter(username__icontains=search)

    paginator = Paginator(users, 10)
    page = request.GET.get('page')
    users_page = paginator.get_page(page)

    return render(request, "medical/pages/show_patient.html", {
        'users': users_page,
        'userprocedure': userprocedure,
    })

# @login_required(login_url='/')
# def create_patient(request):
#     proc = Procedure.objects.all()
#     if request.method == "POST":
#         form = formUser(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.password = make_password(instance.password)
#             instance.user = request.user
#             instance.save()
#             form.save_m2m()
#             return redirect('show_patient')
#     else:
#         form = formUser()
#     return render(request, "medical/pages/create_patient.html", {"formuser": form, "proc": proc})

#     context = {
#         "formuser": form,
#         "proc_with_dates": proc_with_dates,
#     }

#     return render(request, "medical/pages/create_patient.html", context)



def zip_lists(*args):
    return zip(*args)


@login_required(login_url='/')
def delete_patient(request, id):
    user = get_object_or_404(Users, pk=id)
    user.delete()
    return redirect("show_patient")

@login_required(login_url='/')
def update_patient(request, id):
    user = get_object_or_404(Users, id=id)
    form = formUser(instance=user)
    if request.method == 'POST':
        form = formUser(request.POST, instance=user)
        if form.is_valid():
            print("oi")
            form.save()
            return redirect("show_patient")
        else:
            print(form.errors)
    else:
        form = formUser(instance=user)


    return render(request, "medical/pages/update_patient.html",{'user':user, 'form':form})

def config_proc(request,id):
    # userproc = UserProcedure.objects.all()
    filter_proc = UserProcedure.objects.filter(user__id=id)
    return render(request,'medical/pages/config_proc.html',{
        'userproc':filter_proc,
    })
    

def patient_config(request,id):
    userprocs = UserProcedure.objects.all()
    userproc = get_object_or_404(UserProcedure,id=id)

    form = FormUserProcedure(instance=userproc)
    if request.method == 'POST':
        form = FormUserProcedure(request.POST, instance=userproc)
        if form.is_valid():
            print("oi")
            form.save()
            return redirect("config_proc", id=userproc.user.id)

        else:
            print(form.errors)
    else:
        form = FormUserProcedure(instance=userproc)
    return render(request,"medical/pages/patient_config.html",{'form':form,'userprocs':userprocs,'userproc':userproc})


def resetPassword(request):
    return render(request,"medical/pages/resetPassword.html")

@login_required(login_url='/')
def calendar(request):
    return render(request, "medical/pages/calendar.html")


# from datetime import datetime, timedelta
# def patient(request):
#     if request.method == "POST":
#         email = request.POST.get('email')
#         username = request.POST.get('username')
#         cpf = request.POST.get('cpf')
#         birth_date = request.POST.get('birth_date')
#         street = request.POST.get('street')
#         number = request.POST.get('number')
#         district = request.POST.get('district')
#         uf = request.POST.get('uf')
#         phone = request.POST.get('phone')
#         association = request.POST.get('association')
#         bariatric = request.POST.get('bariatric')
#         procedure_ids = request.POST.getlist('procedure')

#         user = Users(
#             email=email,
#             username=username,
#             cpf=cpf,
#             birth_date=birth_date,
#             street=street,
#             number=number,
#             district=district,
#             uf=uf,
#             phone=phone,
#             bariatric=bariatric,
#             association=association
#         )
#         user.save()

#         if procedure_ids:
#             for procedure_id in procedure_ids:
#                 procedure = Procedure.objects.get(id=procedure_id)
#                 nova_date_limit = request.POST.get('date_limit_' + str(procedure_id))
#                 type_procedure = request.POST.get('type_procedure_' + str(procedure_id))
#                 if nova_date_limit:
#                     try:
#                         date_limit = datetime.strptime(nova_date_limit, '%Y-%m-%d').date()
#                     except ValueError:
#                         date_limit = None
#                 else:
#                     days_limit = procedure.days_limit
#                     default_date_limit = date.today() + timedelta(days=days_limit)
#                     date_limit = default_date_limit

#                 user_procedure = UserProcedure(user=user, procedure=procedure, date_limit=date_limit, type_procedure=type_procedure)
#                 user_procedure.save()

#         return redirect('show_patient')

#     return render(request, "medical/pages/patient.html", {
#         'type_procedure_choices': UserProcedure.types_choices,
#         'uf_choices': Users.UF,
#         'association_choices': Users.Association,
#         'procedure_choices': Procedure.objects.all()
#     })



def patient(request):
    if request.method == "POST":
     form = formUser(request.POST)

     if form.is_valid():
        form.save()
        return redirect('show_patient')
    else:
        form = formUser()

    return render(request, "medical/pages/patient.html",{'form': form})



# from django.db.models.signals import m2m_changed
# @receiver(m2m_changed, sender=Users.procedure.through)
# def update_date_limit_userprocedure(sender, instance, action, **kwargs):
#     if action == 'post_add':
#         for procedure in instance.procedure.all():
#             userprocedure = UserProcedure.objects.get(user=instance, procedure=procedure)
#             userprocedure.date_limit = procedure.date_limit
#             userprocedure.save()



