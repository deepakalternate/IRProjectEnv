from django import forms

from .models import Users

# --> SIGN UP FORM <--

class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Password', 'type': 'password'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Re-enter Password', 'type': 'password'}))
    interest1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Interest 1'}))
    interval1 = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Rate Interest [1-10]'}))
    interest2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Interest 2'}))
    interval2 = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Rate Interest [1-10]'}))
    interest3 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Interest 3'}))
    interval3 = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Rate Interest [1-10]'}))

    def clean(self):

        username = self.cleaned_data['username']
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        interval1 = self.cleaned_data['interval1']
        interval2 = self.cleaned_data['interval2']
        interval3 = self.cleaned_data['interval3']

        querieddata = Users.objects.filter(username=username)

        if querieddata:
            raise forms.ValidationError("Username already in use.")

        if password1 != password2:
            raise forms.ValidationError("Entered passwords don't match.")

        if interval1 > 10 or interval2 > 10 or interval3 > 10:
            raise forms.ValidationError("Entered interest values should be between 1 and 10.")

        return self.cleaned_data


# --> LOGIN FORM <--


class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Password', 'type': 'password'}))

    def clean(self):

        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        userdetails = Users.objects.filter(username=username)

        if not userdetails:
            raise forms.ValidationError("Invalid Username")

        for user in userdetails:
            un = user

        if password != un.password:
            raise forms.ValidationError("Incorrect Password")

        return self.cleaned_data


class QueryForm(forms.Form):
    query = forms.CharField()

    def clean(self):
        return self.cleaned_data


class IntimacyForm(forms.Form):
    intimacy = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Rate Intimacy [1-10]'}))

    def clean(self):
        intimacy = self.cleaned_data['intimacy']

        if intimacy > 10:
            raise forms.ValidationError("Enter a value between 1 and 10.")

        return self.cleaned_data