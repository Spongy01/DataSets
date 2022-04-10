from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    username = forms.CharField()


class CreateFolderForm(forms.Form):
    foldername = forms.CharField(max_length=20)
    folderbrief = forms.CharField(max_length=50)
    pathto = forms.CharField()


class CreateTableForm(forms.Form):
    tablename = forms.CharField(max_length=20)
    tablebrief = forms.CharField(max_length=50)