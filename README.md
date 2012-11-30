Django Expand
=============

If you tired to create template files, views etc from scratch every time you created new django model - this app is for you.

Django-expand provides:

* rest templates
* rest views
* urls
* forms

Using
-----

1. Install:

```bash
pip install git+git://github.com/FZambia/django-expand.git
```

2. Add `'expand'` in INSTALLED_APPS

3. Create new django model, ex class Contact in `contact` app:

```python
# contact/models.py
from django.db import models
from django.core.urlresolvers import reverse


class Contact(models.Model):

	first_name = models.CharField(u"contact first name", max_length=30)
	last_name = models.CharField(u"contact last name", max_length=30)
	email = models.EmailField(u"contact email address")
	phone = models.CharField(u"contact phone number", max_length=30)
	created_at = models.DateTimeField(u"created at", auto_now_add=True)
	updated_at = models.DateTimeField(u"updated_at", auto_now=True)

	def __unicode__(self):
		return "%s %s" % (self.first_name, self.last_name)

	def get_absolute_url(self):
		return reverse("contact_contact_detail", kwargs={'pk':self.pk})
```

Note that get_absolute_url method is required and url name must be
constructed from app_label and model_name as follows: "applabel_modelname_detail"

4. Include urls in your application `urls.py`:

```python
url(r'', include('contact.urls')),
```

5. run manage.py command:

```bash
python manage.py expand --app=contact --model=Contact
```

6. Open your browser - go to '/contact/' location and enjoy result!

7. `--append` command line flag can help you to create anothe model from the same app.


Limitations
-----------

This tool is nice for new projects when you do not have any files in app yet.
This is just a start point which helps you to begin and makes some routine 
things instead of you. But nothing more.