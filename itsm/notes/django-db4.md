# Form
### Building a form in Django
- The Form class
> We already know what we want our HTML form to look like. Our starting point for it in Django is this:
```bazaar
from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
```
> A Form instance has an is_valid() method, which runs validation routines for all its fields. When this method is called, if all fields contain valid data, it will:
1. return True
2. place the form’s data in its **cleaned_data** attribute.
> The whole form, when rendered for the first time, will look like:
```bazaar
<label for="your_name">Your name: </label>
<input id="your_name" type="text" name="your_name" maxlength="100" required>
```
> Note that it does not include the <form> tags, or a submit button. We’ll have to provide those ourselves in the template.
- The view
> To handle the form we need to instantiate it in the view for the URL where we want it to be published:
```bazaar
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import NameForm
def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    return render(request, 'name.html', {'form': form})
```
> If we arrive at this view with a GET request, it will create an empty form instance and place it in the template context to be rendered. This is what we can expect to happen the first time we visit the URL.
> If the form is submitted using a POST request, the view will once again create a form instance and populate it with data from the request: form = NameForm(request.POST) This is called “binding data to the form” (it is now a bound form).
> We call the form’s is_valid() method; if it’s not True, we go back to the template with the form. This time the form is no longer empty (unbound) so the HTML form will be populated with the data previously submitted, where it can be edited and corrected as required.
> If is_valid() is True, we’ll now be able to find all the validated form data in its cleaned_data attribute. We can use this data to update the database or do other processing before sending an HTTP redirect to the browser telling it where to go next.
- The template
```bazaar
<form action="/your-name/" method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit" value="Submit">
</form>
```
- More about Django Form classes
  - Bound and unbound form instances
The distinction between Bound and unbound forms is important:
    1. An unbound form has no data associated with it. When rendered to the user, it will be empty or will contain default values.
    2. A bound form has submitted data, and hence can be used to tell if that data is valid. If an invalid bound form is rendered, it can include inline error messages telling the user what data to correct.
  - More on fields
```bazaar
from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
```
  1. Widgets
> Each form field has a corresponding Widget class, which in turn corresponds to an HTML form widget such as <input type="text">.
  2. Field data
> Whatever the data submitted with a form, once it has been successfully validated by calling is_valid() (and is_valid() has returned True), the validated form data will be in the form.cleaned_data dictionary. This data will have been nicely converted into Python types for you.
```bazaar
from django.core.mail import send_mail
if form.is_valid():
    subject = form.cleaned_data['subject']
    message = form.cleaned_data['message']
    sender = form.cleaned_data['sender']
    cc_myself = form.cleaned_data['cc_myself']
    recipients = ['info@example.com']
    if cc_myself:
        recipients.append(sender)
    send_mail(subject, message, sender, recipients)
    return HttpResponseRedirect('/thanks/')
```
- Working with form templates
> All you need to do to get your form into a template is to place the form instance into the template context. So if your form is called form in the context, {{ form }} will render its <label> and <input> elements appropriately.
  1. Reusable form templates
> The HTML output when rendering a form is itself generated via a template. You can control this by creating an appropriate template file and setting a custom FORM_RENDERER to use that form_template_name site-wide. You can also customize per-form by overriding the form’s template_name attribute to render the form using the custom template, or by passing the template name directly to Form.render().
> The example below will result in {{ form }} being rendered as the output of the form_snippet.html template.
```bazaar
# In your template:
{{ form }}

# In form_snippet.html:
{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
    </div>
{% endfor %}
```
> ... used in view:
```bazaar
def index(request):
    form = MyForm()
    rendered_form = form.render("form_snippet.html")
    context = {'form': rendered_form}
    return render(request, 'index.html', context)
```
- Form rendering options
> There are other output options though for the <label>/<input> pairs:
  1. {{ form.as_div }} will render them wrapped in <div> tags.
  2. {{ form.as_table }} will render them as table cells wrapped in <tr> tags.
  3. {{ form.as_p }} will render them wrapped in <p> tags.
  4. {{ form.as_ul }} will render them wrapped in <li> tags.
- Rendering fields manually
> We don’t have to let Django unpack the form’s fields; we can do it manually if we like (allowing us to reorder the fields, for example). Each field is available as an attribute of the form using {{ form.name_of_field }}, and in a Django template, will be rendered appropriately. For example:
```bazaar
{{ form.non_field_errors }}
<div class="fieldWrapper">
    {{ form.subject.errors }}
    <label for="{{ form.subject.id_for_label }}">Email subject:</label>
    {{ form.subject }}
</div>
<div class="fieldWrapper">
    {{ form.message.errors }}
    <label for="{{ form.message.id_for_label }}">Your message:</label>
    {{ form.message }}
</div>
<div class="fieldWrapper">
    {{ form.sender.errors }}
    <label for="{{ form.sender.id_for_label }}">Your email address:</label>
    {{ form.sender }}
</div>
<div class="fieldWrapper">
    {{ form.cc_myself.errors }}
    <label for="{{ form.cc_myself.id_for_label }}">CC yourself?</label>
    {{ form.cc_myself }}
</div>
```
- Looping over the form’s fields
> If you’re using the same HTML for each of your form fields, you can reduce duplicate code by looping through each field in turn using a {% for %} loop:
```bazaar
{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
        {% if field.help_text %}
        <p class="help">{{ field.help_text|safe }}</p>
        {% endif %}
    </div>
{% endfor %}
```
- Looping over hidden and visible fields
> Django provides two methods on a form that allow you to loop over the hidden and visible fields independently: hidden_fields() and visible_fields(). Here’s a modification of an earlier example that uses these two methods:
```bazaar
{# Include the hidden fields #}
{% for hidden in form.hidden_fields %}
{{ hidden }}
{% endfor %}
{# Include the visible fields #}
{% for field in form.visible_fields %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
    </div>
{% endfor %}
```
### Formsets
- class BaseFormSet
> A formset is a layer of abstraction to work with multiple forms on the same page. It can be best compared to a data grid. Let’s say you have the following form:
```bazaar
>>> from django import forms
>>> class ArticleForm(forms.Form):
...     title = forms.CharField()
...     pub_date = forms.DateField()
```
> You might want to allow the user to create several articles at once. To create a formset out of an ArticleForm you would do:
```bazaar
>>> from django.forms import formset_factory
>>> ArticleFormSet = formset_factory(ArticleForm)
```
> As you can see it only displayed one empty form. The number of empty forms that is displayed is controlled by the extra parameter. By default, formset_factory() defines one extra form; the following example will create a formset class to display two blank forms:
```bazaar
>>> ArticleFormSet = formset_factory(ArticleForm, extra=2)
```
- Using initial data with a formset
```bazaar
>>> import datetime
>>> from django.forms import formset_factory
>>> from myapp.forms import ArticleForm
>>> ArticleFormSet = formset_factory(ArticleForm, extra=2)
>>> formset = ArticleFormSet(initial=[
...     {'title': 'Django is now open source',
...      'pub_date': datetime.date.today(),}
... ])
```
> There are now a total of three forms showing above. One for the initial data that was passed in and two extra forms. Also note that we are passing in a list of dictionaries as the initial data.
- Limiting the maximum number of forms
> The max_num parameter to formset_factory() gives you the ability to limit the number of forms the formset will display:
```bazaar
>>> from django.forms import formset_factory
>>> from myapp.forms import ArticleForm
>>> ArticleFormSet = formset_factory(ArticleForm, extra=2, max_num=1)
>>> formset = ArticleFormSet()
```
- Limiting the maximum number of instantiated forms
> The absolute_max parameter to formset_factory() allows limiting the number of forms that can be instantiated when supplying POST data. This protects against memory exhaustion attacks using forged POST requests:
```bazaar
>>> from django.forms.formsets import formset_factory
>>> from myapp.forms import ArticleForm
>>> ArticleFormSet = formset_factory(ArticleForm, absolute_max=1500)
>>> data = {
...     'form-TOTAL_FORMS': '1501',
...     'form-INITIAL_FORMS': '0',
... }
>>> formset = ArticleFormSet(data)
>>> len(formset.forms)
1500
>>> formset.is_valid()
False
>>> formset.non_form_errors()
['Please submit at most 1000 forms.']
```
> When absolute_max is None, it defaults to max_num + 1000. (If max_num is None, it defaults to 2000).
