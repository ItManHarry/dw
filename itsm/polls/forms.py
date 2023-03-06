from django import forms
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=32)
    file = forms.FileField()
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=128)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField(help_text='邮箱地址')
    cc_myself = forms.BooleanField(required=False)