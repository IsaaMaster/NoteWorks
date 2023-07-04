from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control rounded-pill'}))
    #email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control rounded-pill'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control rounded-pill'}))
    #first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    #phone_number = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control'}), required=False)
