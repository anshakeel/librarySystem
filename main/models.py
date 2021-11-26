from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class Account(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Account.objects.create(user_id=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.account.save()

    class Meta:
        db_table = 'account'



class Author(models.Model):
    author_id = models.IntegerField(primary_key=True)
    nationality = models.CharField(max_length=25, blank=True, null=True)
    name = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        db_table = 'author'

    def __str__(self):
        return self.nationality

class Book(models.Model):
    isbn = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=35, blank=True, null=True)
    author = models.CharField(max_length=25, blank=True, null=True)
    genre = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        db_table = 'book'

    def __str__(self):
        return self.title


class Copy(models.Model):
    isbn = models.ForeignKey(Book, models.DO_NOTHING, db_column='isbn', related_name='copy_isbn')
    copy_num = models.IntegerField()

    class Meta:
        db_table = 'copy'

    # def __str__(self):
    #     return self.copy_num

class Librarian(models.Model):
    user = models.ForeignKey(Account, models.DO_NOTHING, related_name='librarian_user')

    class Meta:
        db_table = 'librarian'


class Print(models.Model):
    isbn = models.ForeignKey(Book, models.DO_NOTHING, db_column='isbn', related_name='print_isbn')
    publisher = models.ForeignKey('Publisher', models.DO_NOTHING)

    class Meta:
        db_table = 'print'



class Publisher(models.Model):
    publisher_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=25, blank=True, null=True)
    country = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'publisher'


class Reader(models.Model):
    user = models.ForeignKey(Account, models.SET_NULL, related_name='reader_user', null=True)

    class Meta:
        db_table = 'reader'


class Rent(models.Model):
    user = models.ForeignKey(Reader, models.DO_NOTHING, related_name='rent_user')
    isbn = models.ForeignKey(Copy, models.DO_NOTHING, db_column='isbn', related_name='rent_isbn')
    copy_num = models.IntegerField()
    rent_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'rent'



class Stock(models.Model):
    user = models.ForeignKey(Librarian, models.DO_NOTHING, related_name='stock_user')
    isbn = models.ForeignKey(Copy, models.DO_NOTHING, db_column='isbn', related_name='stock_isbn')
    copy_num = models.BigIntegerField()
    stock_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'stock'



class Write(models.Model):
    isbn = models.ForeignKey(Book, models.DO_NOTHING, db_column='isbn')
    author = models.ForeignKey(Author, models.DO_NOTHING, related_name='author_write')

    class Meta:
        db_table = 'write'

