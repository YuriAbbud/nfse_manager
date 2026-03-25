from django.urls import path
from . import views

urlpatterns = [
    # ─── Dashboard ───────────────────────────────
    path('', views.dashboard, name='dashboard'),

    # ─── Clientes ────────────────────────────────
    path('clientes/', views.cliente_lista, name='cliente_lista'),
    path('clientes/novo/', views.cliente_criar, name='cliente_criar'),
    path('clientes/<int:pk>/editar/', views.cliente_editar, name='cliente_editar'),
    path('clientes/<int:pk>/excluir/', views.cliente_excluir, name='cliente_excluir'),

    # ─── Notas Fiscais ────────────────────────────
    path('notas/', views.nota_lista, name='nota_lista'),
    path('notas/nova/', views.nota_criar, name='nota_criar'),
    path('notas/<int:pk>/excluir/', views.nota_excluir, name='nota_excluir'),
]