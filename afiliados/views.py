from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Afiliado, ContratoAfiliacao
from .forms import AfiliadoForm, AfiliadoEditForm


@login_required
def cadastro_afiliado(request):
    try:
        perfil = request.user.perfil
    except request.user._meta.model.perfil.RelatedObjectDoesNotExist:
        messages.error(request, 'Perfil de usuário não encontrado.')
        return redirect('home')
    
    
    if perfil.tipo_usuario != 'AFILIADO':
        messages.error(request, 'Acesso negado. Apenas afiliados podem acessar esta página.')
        return redirect('core_dashboard:dashboard')
    
    
    if hasattr(perfil, 'dados_afiliado'):
        messages.info(request, 'Você já possui cadastro completo.')
        return redirect('afiliados:meu_perfil')
    
    if request.method == 'POST':
        form = AfiliadoForm(request.POST)
        if form.is_valid():
            afiliado = form.save(commit=False)
            afiliado.perfil = perfil
            afiliado.save()
            
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('core_dashboard:dashboard')
    else:
        form = AfiliadoForm()
    
    context = {
        'form': form,
        'titulo': 'Completar Cadastro de Afiliado'
    }
    return render(request, 'afiliados/cadastro_afiliado.html', context)


@login_required
def meu_perfil_afiliado(request):
    perfil = request.user.perfil
    
    if perfil.tipo_usuario != 'AFILIADO':
        messages.error(request, 'Acesso negado.')
        return redirect('core_dashboard:dashboard')
    
    if not hasattr(perfil, 'dados_afiliado'):
        messages.warning(request, 'Complete seu cadastro primeiro.')
        return redirect('afiliados:cadastro_afiliado')
    
    afiliado = perfil.dados_afiliado
    contratos = afiliado.contratos.all()
    contrato_ativo = contratos.filter(status='ativo').first()
    
    context = {
        'afiliado': afiliado,
        'contratos': contratos,
        'contrato_ativo': contrato_ativo,
    }
    return render(request, 'afiliados/meu_perfil.html', context)


@login_required
def editar_afiliado(request):
    perfil = request.user.perfil
    
    if perfil.tipo_usuario != 'AFILIADO':
        messages.error(request, 'Acesso negado.')
        return redirect('core_dashboard:dashboard')
    
    afiliado = get_object_or_404(Afiliado, perfil=perfil)
    
    if request.method == 'POST':
        form = AfiliadoEditForm(request.POST, instance=afiliado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados atualizados com sucesso!')
            return redirect('afiliados:meu_perfil')
    else:
        form = AfiliadoEditForm(instance=afiliado)
    
    context = {
        'form': form,
        'afiliado': afiliado,
        'titulo': 'Editar Meus Dados'
    }
    return render(request, 'afiliados/editar_afiliado.html', context)


@login_required
def contratos_afiliado(request):
    perfil = request.user.perfil
    
    if perfil.tipo_usuario != 'AFILIADO':
        messages.error(request, 'Acesso negado.')
        return redirect('core_dashboard:dashboard')
    
    if not hasattr(perfil, 'dados_afiliado'):
        messages.warning(request, 'Complete seu cadastro primeiro.')
        return redirect('afiliados:cadastro_afiliado')
    
    afiliado = perfil.dados_afiliado
    contratos = afiliado.contratos.all()
    
    context = {
        'contratos': contratos,
        'afiliado': afiliado,
    }
    return render(request, 'afiliados/contratos.html', context)


@login_required
def aceitar_contrato(request, contrato_id):
    perfil = request.user.perfil
    
    if perfil.tipo_usuario != 'AFILIADO':
        messages.error(request, 'Acesso negado.')
        return redirect('core_dashboard:dashboard')
    
    afiliado = get_object_or_404(Afiliado, perfil=perfil)
    contrato = get_object_or_404(ContratoAfiliacao, id=contrato_id, afiliado=afiliado)
    
    if contrato.termo_aceito:
        messages.info(request, 'Este contrato já foi aceito.')
        return redirect('afiliados:contratos')
    
    if request.method == 'POST':
        contrato.termo_aceito = True
        contrato.data_aceite = timezone.now()
        contrato.ip_aceite = request.META.get('REMOTE_ADDR')
        contrato.status = 'ativo'
        contrato.save()
        
        messages.success(request, 'Contrato aceito com sucesso!')
        return redirect('afiliados:meu_perfil')
    
    context = {
        'contrato': contrato,
        'afiliado': afiliado,
    }
    return render(request, 'afiliados/aceitar_contrato.html', context)