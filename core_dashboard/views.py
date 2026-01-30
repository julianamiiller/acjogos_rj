from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q

from core_dashboard.models import (
    Notificacao,
    AtividadeRecente,
    ConfiguracaoDashboard,
    MenuFavorito
)
from perfis.models import Perfil
from coletivos.models import Coletivo


@login_required
def dashboard(request):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        messages.error(
            request,
            'Seu perfil de usuário não foi encontrado. Por favor, entre em contato com o suporte.'
        )
        return redirect('home')

    config, created = ConfiguracaoDashboard.objects.get_or_create(perfil=perfil)

    notificacoes_nao_lidas = Notificacao.objects.filter(
        perfil=perfil,
        lida=False
    ).order_by('-data_criacao')[:5]

    atividades_recentes = (
        AtividadeRecente.objects.filter(perfil=perfil)
        .order_by('-data_criacao')[:10]
        if config.exibir_atividades_recentes
        else None
    )

    favoritos = MenuFavorito.objects.filter(perfil=perfil)

    estatisticas = {}

    if perfil.tipo_usuario == 'ASSOCIADO':
        if hasattr(perfil, 'empresa'):
            estatisticas['possui_empresa'] = True
            estatisticas['empresa'] = perfil.empresa
        else:
            estatisticas['possui_empresa'] = False

    elif perfil.tipo_usuario == 'AFILIADO':
        if hasattr(perfil, 'dados_afiliado'):
            afiliado = perfil.dados_afiliado
            contratos = afiliado.contratos.all()
            estatisticas['total_contratos'] = contratos.count()
            estatisticas['contratos_ativos'] = contratos.filter(status='ativo').count()
            estatisticas['cadastro_completo'] = True
        else:
            estatisticas['cadastro_completo'] = False

    elif perfil.tipo_usuario == 'DIRETOR':
        from django.contrib.auth.models import User
        from empresas.models import Empresa

        estatisticas['total_usuarios'] = User.objects.count()
        estatisticas['pendentes_aprovacao'] = Perfil.objects.filter(status='PENDENTE').count()
        estatisticas['total_empresas'] = Empresa.objects.count()
        estatisticas['total_coletivos'] = Coletivo.objects.count()

    elif perfil.tipo_usuario == 'COLETIVO':
        if hasattr(perfil, 'dados_coletivo'):
            coletivo = perfil.dados_coletivo
            estatisticas['instituicao'] = coletivo

            membros_grupo = Perfil.objects.filter(coletivo_padrinho=coletivo)
            estatisticas['total_membros'] = membros_grupo.count()

            from empresas.models import Empresa
            estatisticas['total_empresas'] = Empresa.objects.filter(
                perfil__in=membros_grupo
            ).count()

            estatisticas['pendencias'] = membros_grupo.filter(status='PENDENTE').count()
        else:
            estatisticas['instituicao'] = None

    context = {
        'perfil': perfil,
        'config': config,
        'notificacoes': notificacoes_nao_lidas,
        'atividades': atividades_recentes,
        'favoritos': favoritos,
        'estatisticas': estatisticas,
    }

    if perfil.tipo_usuario == 'ASSOCIADO':
        return render(request, 'dashboard/dashboard_associado.html', context)
    elif perfil.tipo_usuario == 'AFILIADO':
        return render(request, 'dashboard/dashboard_afiliado.html', context)
    elif perfil.tipo_usuario == 'DIRETOR':
        return render(request, 'dashboard/dashboard_diretoria.html', context)
    elif perfil.tipo_usuario == 'COLETIVO':
        return render(request, 'dashboard/dashboard_coletivo.html', context)
    else:
        return render(request, 'dashboard/dashboard_base.html', context)


@login_required
def notificacoes(request):
    perfil = request.user.perfil
    filtro = request.GET.get('filtro', 'todas')

    notificacoes_list = Notificacao.objects.filter(perfil=perfil)

    if filtro == 'nao_lidas':
        notificacoes_list = notificacoes_list.filter(lida=False)
    elif filtro == 'lidas':
        notificacoes_list = notificacoes_list.filter(lida=True)

    notificacoes_list = notificacoes_list.order_by('-data_criacao')

    total = Notificacao.objects.filter(perfil=perfil).count()
    nao_lidas = Notificacao.objects.filter(perfil=perfil, lida=False).count()

    context = {
        'notificacoes': notificacoes_list,
        'filtro': filtro,
        'total': total,
        'nao_lidas': nao_lidas,
        'perfil': perfil,
    }
    return render(request, 'dashboard/notificacoes.html', context)


@login_required
def marcar_notificacao_lida(request, notificacao_id):
    perfil = request.user.perfil
    notificacao = get_object_or_404(
        Notificacao,
        id=notificacao_id,
        perfil=perfil
    )

    notificacao.marcar_como_lida()

    if notificacao.link:
        return redirect(notificacao.link)

    return redirect('core_dashboard:notificacoes')


@login_required
def marcar_todas(request):
    perfil = request.user.perfil

    Notificacao.objects.filter(
        perfil=perfil,
        lida=False
    ).update(
        lida=True,
        data_leitura=timezone.now()
    )

    messages.success(
        request,
        'Todas as notificações foram marcadas como lidas.'
    )
    return redirect('core_dashboard:notificacoes')


@login_required
def atividades(request):
    perfil = request.user.perfil
    acao = request.GET.get('acao')

    atividades_list = AtividadeRecente.objects.filter(perfil=perfil)

    if acao:
        atividades_list = atividades_list.filter(acao=acao)

    atividades_list = atividades_list.order_by('-data_criacao')

    context = {
        'atividades': atividades_list,
        'acao_selecionada': acao,
        'tipos_acao': AtividadeRecente.ACAO_CHOICES,
        'perfil': perfil,
    }
    return render(request, 'dashboard/atividades.html', context)


@login_required
def configuracoes(request):
    perfil = request.user.perfil
    config, created = ConfiguracaoDashboard.objects.get_or_create(perfil=perfil)

    if request.method == 'POST':
        config.exibir_atividades_recentes = request.POST.get('exibir_atividades_recentes') == 'on'
        config.exibir_notificacoes = request.POST.get('exibir_notificacoes') == 'on'
        config.exibir_estatisticas = request.POST.get('exibir_estatisticas') == 'on'
        config.exibir_atalhos = request.POST.get('exibir_atalhos') == 'on'
        config.notificacoes_email = request.POST.get('notificacoes_email') == 'on'
        config.notificacoes_push = request.POST.get('notificacoes_push') == 'on'

        tema = request.POST.get('tema')
        if tema in ['claro', 'escuro', 'auto']:
            config.tema = tema

        itens = request.POST.get('itens_por_pagina')
        if itens and itens.isdigit():
            config.itens_por_pagina = int(itens)

        config.save()
        messages.success(request, 'Configurações atualizadas com sucesso!')
        return redirect('core_dashboard:configuracoes')

    return render(
        request,
        'dashboard/configuracoes.html',
        {'perfil': perfil, 'config': config}
    )


@login_required
def adicionar_favorito(request):
    if request.method == 'POST':
        perfil = request.user.perfil
        nome = request.POST.get('nome')
        url = request.POST.get('url')
        icone = request.POST.get('icone', '')

        if nome and url:
            if not MenuFavorito.objects.filter(perfil=perfil, url=url).exists():
                MenuFavorito.objects.create(
                    perfil=perfil,
                    nome=nome,
                    url=url,
                    icone=icone
                )
                messages.success(request, f'"{nome}" adicionado aos favoritos!')
            else:
                messages.info(request, 'Este item já está nos favoritos.')
        else:
            messages.error(request, 'Nome e URL são obrigatórios.')

    return redirect('core_dashboard:dashboard')


@login_required
def remover_favorito(request, favorito_id):
    perfil = request.user.perfil
    favorito = get_object_or_404(
        MenuFavorito,
        id=favorito_id,
        perfil=perfil
    )

    nome = favorito.nome
    favorito.delete()

    messages.success(request, f'"{nome}" removido dos favoritos.')
    return redirect('core_dashboard:dashboard')


def registrar_atividade(perfil, acao, descricao, request=None, detalhes=''):
    ip_address = None
    user_agent = ''

    if request:
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')

    AtividadeRecente.objects.create(
        perfil=perfil,
        acao=acao,
        descricao=descricao,
        detalhes=detalhes,
        ip_address=ip_address,
        user_agent=user_agent
    )


def criar_notificacao(perfil, titulo, mensagem, tipo='info', link=''):
    Notificacao.objects.create(
        perfil=perfil,
        titulo=titulo,
        mensagem=mensagem,
        tipo=tipo,
        link=link
    )
