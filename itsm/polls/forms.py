from django import forms
class UploadFileForm(forms.Form):
    BIRTH_YEAR = ['1980', '1981', '1982', '1983']
    COLOR_FOR_CHOICE = [
        ('red', 'RED'),
        ('blue', 'BLUE'),
        ('black', 'BLACK'),
        ('yellow', 'YELLOW'),
    ]
    CHOICES = [('1', 'YES'), ('2', 'NO')]
    choice = forms.ChoiceField(label='选择', widget=forms.RadioSelect, choices=CHOICES)
    birth_year = forms.DateField(label='生日', widget=forms.SelectDateWidget(years=BIRTH_YEAR))
    favorite_color = forms.MultipleChoiceField(label='颜色爱好', required=False, widget=forms.CheckboxSelectMultiple(), choices=COLOR_FOR_CHOICE)
    title = forms.CharField(label='标题', max_length=32)
    file = forms.FileField(label='文件')

class FileFieldForm(forms.Form):
    file_field = forms.FileField(label='附件', help_text='可以选择多个文件进行上传！', widget=forms.ClearableFileInput(attrs={'multiple': True}))
class ContactForm(forms.Form):
    BIRTH_YEAR = ['1980', '1981', '1982', '1983']
    COLOR_FOR_CHOICE = [
        ('red', 'RED'),
        ('blue', 'BLUE'),
        ('black', 'BLACK'),
        ('yellow', 'YELLOW'),
    ]
    CHOICES = [('1', 'YES'), ('2', 'NO')]
    id = forms.CharField(widget=forms.HiddenInput(), initial='123456')
    choice = forms.ChoiceField(label='选择', widget=forms.RadioSelect, choices=CHOICES)
    birth_year = forms.DateField(label='生日', widget=forms.SelectDateWidget(years=BIRTH_YEAR, attrs={'class': 'form-control'}))
    favorite_color = forms.MultipleChoiceField(label='颜色爱好', required=False, widget=forms.CheckboxSelectMultiple(), choices=COLOR_FOR_CHOICE)
    subject = forms.CharField(label='主题', max_length=128, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '邮件主题'}))
    message = forms.CharField(label='消息', widget=forms.Textarea(attrs={'class': 'form-control'}))
    sender = forms.EmailField(label='邮箱', help_text='邮箱地址(xxx@xxx.xx)', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    cc_myself = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))