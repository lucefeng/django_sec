from django import forms

class registerForm(forms.Form):
    register_name = forms.CharField()
    register_email = forms.EmailField(required=True)
    register_gender = forms.CharField()
    register_psw = forms.CharField()
    def clean_email(self):
        email = self.cleaned_data['email']
        if email == "123@1" :
            raise forms.ValidationError("email地址不能为空")
        return email
class ContactForm(forms.Form):
    subject = forms.CharField(min_length=4, max_length=20)
    email = forms.EmailField(required=False)
    message = forms.CharField(min_length=4, max_length=20)
    def clean_email(self):
        email = self.cleaned_data['email']
        if email == "123@1.com" :
            raise forms.ValidationError("email地址不能为空")
        return email

