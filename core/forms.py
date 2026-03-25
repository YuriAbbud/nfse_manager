from django import forms
from .models import Cliente, NotaFiscal


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['nome', 'cpf_cnpj', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo ou Razão Social'
            }),
            'cpf_cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Somente números — 11 (CPF) ou 14 (CNPJ)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemplo@email.com'
            }),
        }

    def clean_cpf_cnpj(self):
        # Validação CPF/CNPJ

        cpf_cnpj = self.cleaned_data.get('cpf_cnpj')

        cpf_cnpj = cpf_cnpj.strip()

        if not cpf_cnpj.isdigit():
            raise forms.ValidationError(
                "Digite apenas números, sem pontos ou traços."
            )

        if len(cpf_cnpj) not in [11, 14]:
            raise forms.ValidationError(
                "CPF deve ter 11 dígitos e CNPJ deve ter 14 dígitos."
            )

        return cpf_cnpj


class NotaFiscalForm(forms.ModelForm):
    # Formulário para emissão de notas fiscais.
    
    class Meta:
        model = NotaFiscal
        fields = ['cliente', 'descricao_servico', 'valor_bruto']
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-select',
            }),
            'descricao_servico': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva o serviço prestado...'
            }),
            'valor_bruto': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01'
            }),
        }