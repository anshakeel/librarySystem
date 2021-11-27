from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Reader)
admin.site.register(Account)
admin.site.register(Stock)
admin.site.register(Book)
admin.site.register(Librarian)
admin.site.register(Copy)
admin.site.register(Rent)
admin.site.register(Publisher)
admin.site.register(Write)
admin.site.register(Print)
admin.site.register(Author)
