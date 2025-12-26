from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CadastroUsuarioForm

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('login')
        else:
            print(form.errors) 
    else:
        form = CadastroUsuarioForm()
    return render(request, 'registration/cadastro.html', {'form': form})