from django.db import models
from datetime import datetime
import bcrypt

class UserManager(models.Manager):
    def registration_validator(self, post_data):
        errors = {}
        if len(post_data['name']) < 3:
            errors['name'] = "Your last must be more than 2 characters"
        if User.objects.filter(username=post_data['username']).exists():
            errors['username'] = "Username already exists"
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be more than 8 characters"
        if  post_data['password'] != post_data['password_confirm']:
            errors['password_confirm'] = "Passwords do not match"
        return errors
    def login_validator(self, post_data):
        errors = {}
        if len(post_data['login_username']) < 1:
            errors['login_username'] = "Username is required"
        if len(post_data['login_password']) < 1:
            errors['login_password'] = "Password is required"
        if not User.objects.filter(username=post_data['login_username']):
            errors['login_username'] = "Invalid username"
        else:
            user = User.objects.get(username=post_data['login_username'])
            if not bcrypt.checkpw(post_data['login_password'].encode(), user.password.encode()):
                errors['password'] = "Login password is not valid"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class TripManager(models.Manager):
    def trip_validator(self, post_data):
        errors = {}
        if len(post_data['destination']) < 1:
            errors['destination'] = "Destination must not be empty"
        if len(post_data['description']) < 1:
            errors['description'] = "Description must not be empty"
        if not post_data['start_date']:
            errors['start'] = "Travel Date From must not be empty"
        if not post_data['start_date']:
            errors['end'] = "Travel Date To must not be empty"
        if post_data['start_date'] < str(datetime.now()):
            errors['start_date'] = "Travel date from must be in the future"
        if post_data['start_date'] > post_data['end_date']:
            errors['end_date'] = "Travel Date To must not be before Travel Date From"
        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    creator = models.ForeignKey(User, related_name="trips_planned", on_delete=models.CASCADE)
    joining = models.ManyToManyField(User, related_name="other_trips")
    objects = TripManager()