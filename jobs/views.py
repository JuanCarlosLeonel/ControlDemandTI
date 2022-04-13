from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from . models import Jobs, Referencias, User
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from .form import JobForm

@login_required(login_url='/auth/logar')
def encontrar_jobs(request):
    if request.method == "GET":
        prazo_minimo = request.GET.get('prazo_minimo')
        prazo_maximo = request.GET.get('prazo_maximo')
        categoria = request.GET.get('categoria')

        if  prazo_minimo or prazo_maximo or categoria:
            if not prazo_minimo:
                prazo_minimo = datetime(year=1900, month=1, day=1)
            if not prazo_maximo:
                prazo_maximo = datetime(year=3000, month=1, day=1)
            if categoria == 'M':
                categoria = ['M',]
            elif categoria == 'ND':
                categoria = ['ND',]
            jobs = Jobs.objects.filter(prazo_entrega__gte=prazo_minimo)\
                                .filter(prazo_entrega__lte=prazo_maximo)\
                                .filter(categoria__in=categoria)\
                                .filter(reservado=False)
        else:
            jobs = Jobs.objects.filter(reservado = False)
        return render(request, 'encontrar_jobs.html', {'jobs': jobs})


@login_required(login_url='/auth/logar')
def aceitar_job(request, id):
    job = Jobs.objects.get(id=id)
    job.profissional = request.user
    job.reservado = True
    job.save()
    return redirect('encontrar_jobs')


@login_required(login_url='/auth/logar')
def perfil(request):
    if request.method == "GET":
        jobs = Jobs.objects.filter(profissional=request.user)
        return render(request, 'perfil.html', {'jobs': jobs})
    elif request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')

        usuario = User.objects.filter(username=username).exclude(id=request.user.id)

        if usuario.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse Username')
            return redirect('perfil')

        usuario = User.objects.filter(email=email).exclude(id=request.user.id)

        if usuario.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse E-mail')
            return redirect('perfil')

        request.user.username = username
        request.user.email = email
        request.user.first_name = primeiro_nome
        request.user.last_name = ultimo_nome
        request.user.save()

        messages.add_message(request, constants.SUCCESS, 'Dados alterado com sucesso')
        return redirect('perfil')

@login_required(login_url='/auth/logar')
def enviar_projeto(request):
    arquivo = request.FILES.get('file')
    id_job = request.POST.get('id')

    job = Jobs.objects.get(id=id_job)

    job.arquivo_final = arquivo
    job.status = 'AA'
    job.save()
    return redirect('perfil')


class CreateJob(CreateView):
    form_class = JobForm
    template_name = 'jobs_form.html'
    model = Jobs

    def get_success_url(self):
        return 'perfil' 

    def get_initial(self, *args, **kwargs):
        import datetime
        initial = super(CreateJob, self).get_initial(**kwargs)
        initial['prazo_entrega'] = datetime.date.today()
        return initial



