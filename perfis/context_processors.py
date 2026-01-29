from .models import Perfil

def perfil_context_processor(request):
    """
    Injeta o objeto 'perfil' em todos os templates do projeto 
    sempre que o usuário estiver logado.
    """
    if request.user.is_authenticated:
        try:
            return {'perfil': request.user.perfil}
        except Perfil.DoesNotExist:
            return {'perfil': None}
    return {'perfil': None}
