from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EmpresaForm

@login_required
def empresa_cadastrar_view(request):
    perfil = request.user.perfil

    # 🔒 Segurança: só ASSOCIADO pode acessar
    if perfil.tipo_usuario != 'ASSOCIADO':
        return redirect('home')

    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.perfil = perfil
            empresa.save()
            return redirect('home')
    else:
        form = EmpresaForm()

    return render(request, 'empresas/empresa_form.html', {'form': form})
