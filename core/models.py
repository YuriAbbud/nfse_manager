from django.db import models
from decimal import Decimal

# Create your models here.

class Cliente(models.Model):
    #Representa um cliente cadastrado no sistema. Pode ser pessoa física (CPF - 11 dígitos) ou jurídica (CNPJ - 14 dígitos)
    
    nome = models.CharField(
        max_length=200,
        verbose_name="Nome completo / Razão Social"
    )
    cpf_cnpj = models.CharField(
        max_length=14,
        unique=True,
        verbose_name="CPF / CNPJ"
    )
    email = models.EmailField(
        verbose_name="E-mail"
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Cadastrado em"
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.cpf_cnpj})"


class NotaFiscal(models.Model):
    # Representa uma Nota Fiscal de Serviço emitida para um cliente. O ISS é sempre 5% do valor bruto e calculado automaticamente.

    ALIQUOTA_ISS = Decimal(0.05)

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='notas',
        verbose_name="Cliente"
    )
    descricao_servico = models.TextField(
        verbose_name="Descrição do Serviço"
    )
    valor_bruto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor Bruto (R$)"
    )
    valor_iss = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        verbose_name="Valor ISS (R$)"
    )
    emitida_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Emissão"
    )

    class Meta:
        verbose_name = "Nota Fiscal"
        verbose_name_plural = "Notas Fiscais"
        ordering = ['-emitida_em']

    def save(self, *args, **kwargs):
        # Sempre que salvar uma nota, recalcula o ISS automaticamente
        self.valor_iss = self.valor_bruto * self.ALIQUOTA_ISS
        super().save(*args, **kwargs)

    def __str__(self):
        return f"NFS-e #{self.pk} — {self.cliente.nome} — R$ {self.valor_bruto}"