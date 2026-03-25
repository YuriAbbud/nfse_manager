from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from .models import Cliente, NotaFiscal
from .forms import ClienteForm, NotaFiscalForm

# Create your views here.

# ─────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────

def dashboard(request):
    """
    Página inicial com os cards de resumo financeiro.
    Calcula totais diretamente do banco de dados.
    """
    total_notas = NotaFiscal.objects.count()

    # aggregate() faz cálculos direto no banco — mais eficiente que somar em Python
    resultado = NotaFiscal.objects.aggregate(
        faturamento=Sum('valor_bruto'),
        total_iss=Sum('valor_iss')
    )

    faturamento_total = resultado['faturamento'] or 0
    total_iss = resultado['total_iss'] or 0

    # As últimas 5 notas para exibir no dashboard
    ultimas_notas = NotaFiscal.objects.select_related('cliente')[:5]

    contexto = {
        'total_notas': total_notas,
        'faturamento_total': faturamento_total,
        'total_iss': total_iss,
        'ultimas_notas': ultimas_notas,
    }
    return render(request, 'core/dashboard.html', contexto)


# ─────────────────────────────────────────
# CLIENTES
# ─────────────────────────────────────────

def cliente_lista(request):
    """
    Lista todos os clientes cadastrados.
    """
    clientes = Cliente.objects.all()
    return render(request, 'core/cliente_lista.html', {'clientes': clientes})


def cliente_criar(request):
    """
    Exibe e processa o formulário de cadastro de cliente.
    GET  → exibe o formulário vazio
    POST → valida e salva os dados
    """
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Cliente cadastrado com sucesso!')
            return redirect('cliente_lista')
        else:
            messages.error(request, '❌ Corrija os erros abaixo.')
    else:
        form = ClienteForm()

    return render(request, 'core/cliente_form.html', {'form': form, 'titulo': 'Novo Cliente'})


def cliente_editar(request, pk):
    """
    Edita um cliente existente.
    Usa get_object_or_404 — se o cliente não existir, mostra página 404.
    """
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Cliente atualizado com sucesso!')
            return redirect('cliente_lista')
        else:
            messages.error(request, '❌ Corrija os erros abaixo.')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'core/cliente_form.html', {'form': form, 'titulo': 'Editar Cliente'})


def cliente_excluir(request, pk):
    """
    Exclui um cliente — mas só se não tiver notas vinculadas.
    O PROTECT no Model já bloqueia, mas tratamos o erro aqui.
    """
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        try:
            cliente.delete()
            messages.success(request, '✅ Cliente excluído com sucesso!')
        except Exception:
            messages.error(request, '❌ Este cliente possui notas fiscais e não pode ser excluído.')
        return redirect('cliente_lista')

    return render(request, 'core/cliente_confirmar_exclusao.html', {'objeto': cliente})


# ─────────────────────────────────────────
# NOTAS FISCAIS
# ─────────────────────────────────────────

def nota_lista(request):
    """
    Lista todas as notas fiscais emitidas.
    select_related('cliente') evita consultas extras ao banco — boa prática!
    """
    notas = NotaFiscal.objects.select_related('cliente').all()
    return render(request, 'core/nota_lista.html', {'notas': notas})


def nota_criar(request):
    """
    Emite uma nova nota fiscal.
    O ISS é calculado automaticamente no save() do Model.
    """
    if request.method == 'POST':
        form = NotaFiscalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Nota fiscal emitida com sucesso!')
            return redirect('nota_lista')
        else:
            messages.error(request, '❌ Corrija os erros abaixo.')
    else:
        form = NotaFiscalForm()

    return render(request, 'core/nota_form.html', {'form': form, 'titulo': 'Emitir Nota Fiscal'})


def nota_excluir(request, pk):
    """
    Exclui uma nota fiscal.
    """
    nota = get_object_or_404(NotaFiscal, pk=pk)

    if request.method == 'POST':
        nota.delete()
        messages.success(request, '✅ Nota fiscal excluída com sucesso!')
        return redirect('nota_lista')

    return render(request, 'core/nota_confirmar_exclusao.html', {'objeto': nota})