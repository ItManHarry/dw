from django import forms

class ArticleForm(forms.Form):
    title = forms.CharField(label='标题', required=True)
    pub_date = forms.DateField(label='发布日期', required=True)
