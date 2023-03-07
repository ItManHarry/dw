from django import forms
class UploadFileForm(forms.Form):
    title = forms.CharField(label='标题', max_length=32)
    file = forms.FileField(label='文件')
class FileFieldForm(forms.Form):
    file_field = forms.FileField(label='附件', help_text='可以选择多个文件进行上传！', widget=forms.ClearableFileInput(attrs={'multiple': True}))
class ContactForm(forms.Form):
    subject = forms.CharField(label='主题', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='消息', widget=forms.Textarea(attrs={'class': 'form-control'}))
    sender = forms.EmailField(label='邮箱', help_text='邮箱地址(xxx@xxx.xx)', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    cc_myself = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))