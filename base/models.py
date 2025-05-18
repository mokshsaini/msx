from django.db import models
# from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from sysauth.models import User
# Create your models here.


# class User(models.Model):
#     username = models.CharField(unique=True, max_length=20,
#         validators=[MinLengthValidator(8, 'username must contain at least 8 characters')]
#         )
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=20,
#         validators=[MinLengthValidator(4, 'Password must contain at least 4 characters')]
#      )

#     def __str__(self):
#         return self.username


class Category(models.Model):
    category = models.CharField(validators=[MinLengthValidator(2)], max_length=20)

    def __str__(self):
        return self.category

class Listing(models.Model):
    title = models.CharField(validators=[MinLengthValidator(2)])
    description = models.TextField(validators=[MinLengthValidator(2)], max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    minimum_bidvalue = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
         return self.title


class Comment(models.Model):
    comment = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    listing = models.ManyToManyField(Listing)


class Bid(models.Model):
    bidvalue = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

