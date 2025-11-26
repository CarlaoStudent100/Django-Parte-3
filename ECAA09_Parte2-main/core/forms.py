from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Problema, PerfilOficina, Especialidade

# 1. Formulário para Cadastro de Cliente
class ClienteSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_cliente = True
        if commit:
            user.save()
        return user

# 2. Formulário para Cadastro de Usuário da Oficina
class OficinaSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_oficina = True
        if commit:
            user.save()
        return user

# 3. Formulário para Criar/Editar Problemas (COM IMAGEM)
class ProblemaForm(forms.ModelForm):
    class Meta:
        model = Problema
        # O CAMPO 'imagem' PRECISA ESTAR NESTA LISTA ABAIXO:
        fields = ['titulo', 'modelo_carro', 'descricao', 'imagem']
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Motor falhando'}),
            'modelo_carro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Fiat Uno 2010'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descreva o problema...'}),
            # O widget abaixo garante que o campo apareça bonito com Bootstrap
            'imagem': forms.FileInput(attrs={'class': 'form-control'}),
        }

# 4. Formulário para Perfil da Oficina
class OficinaPerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilOficina
        fields = ['nome_oficina', 'endereco', 'especialidades']
        widgets = {
            'nome_oficina': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidades': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }