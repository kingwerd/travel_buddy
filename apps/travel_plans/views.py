from django.shortcuts import render, redirect
from django.contrib import messages

import bcrypt
from datetime import datetime

from .models import User, Trip

def main(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return render(request, 'travel_plans/login_registration.html')

def register_user(request):
    if request.method == "GET":
        return redirect('/')
    if request.method == "POST":
        data = request.POST
        errors = User.objects.registration_validator(data)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = data['password'].encode()
            password = bcrypt.hashpw(password, bcrypt.gensalt()).decode()
            user = User.objects.create(name=data['name'], username=data['username'], password=password)
            user.save()
            request.session['user_id'] = user.id
            context = {
                'user': user
            }
            return redirect('/travels')

def login_user(request):
    if request.method == "GET":
            return redirect('/')
    if request.method == "POST":
        data = request.POST
        errors = User.objects.login_validator(data)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = User.objects.get(username=data['login_username'])
            request.session['user_id'] = user.id
            return redirect('/travels')


def show_trips(request):
    if not 'user_id' in request.session:
        return redirect('/')
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    user_trips = Trip.objects.filter(creator__id=user_id) | Trip.objects.filter(joining__id=user_id)
    other_trips = Trip.objects.exclude(creator__id=user_id) &  Trip.objects.exclude(joining__id=user_id)
    context = {
        'user': user,
        'your_trips': user_trips,
        'other_trips': other_trips
    }
    return render(request, 'travel_plans/dashboard.html', context)

def join_trip(request, id):
    if not 'user_id' in request.session:
        return redirect('/')
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    trip_to_join = Trip.objects.get(id=id)
    trip_to_join.joining.add(user)
    user.other_trips.add(trip_to_join)
    return redirect('/travels')

def show_destination(request, id):
    if not 'user_id' in request.session:
        return redirect('/')
    trip = Trip.objects.get(id=id)
    context = {
        'trip': trip
    }
    return render(request, 'travel_plans/show_trip.html', context)

def add_trip(request):
    if not 'user_id' in request.session:
        return redirect('/')
    if request.method == "GET":
        return render(request, 'travel_plans/add_trip.html')
    if request.method == "POST":
        data = request.POST
        errors = Trip.objects.trip_validator(data)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/travels/add')
        else:
            user_id = request.session['user_id']
            user = User.objects.get(id=user_id)
            trip = Trip.objects.create(destination=data['destination'], description=data['description'], date_from=data['start_date'], date_to=data['end_date'], creator=user)
            return redirect('/travels')

def logout(request):
    del request.session['user_id']
    return redirect('/')