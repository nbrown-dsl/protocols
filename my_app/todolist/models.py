from django.db import models
from django.db.models.fields.related import ForeignKey
from django.forms.forms import Form 

# CREATE DATABASE MIGRATION: python manage.py makemigrations
# MIGRATE THE DATABASE: python manage.py migrate #
# use in terminal from 'todo_list.models import List' to query list table #

# create database table with attributes.

class persons(models.Model):
    name =  models.CharField(max_length=200)
    email = models.CharField(max_length=400,default='')   
    # so that name appears in select field
    def __str__(self): 
         return self.name
    
class List(models.Model):
    forename =  models.CharField(max_length=50,default='')
    surname = models.CharField(max_length=50,default='')
    YEAR_LEVELS = (
    ('1', 'yr 1'),
    ('2', 'yr 2'),
    ('3', 'yr 3')
    )
    yearLevel = models.CharField(max_length=1, choices=YEAR_LEVELS,default='')
    completed = models.BooleanField(default=False)
    arrivalDate = models.DateField(null=True)
    leavingDate = models.DateField(null=True)
    people = models.ManyToManyField(persons)

    def __str__(self):
        return self.item + ' completed: ' + str(self.completed)


class protocolType(models.Model):
    protocolTypeName =  models.CharField(max_length=100,)
    description =  models.CharField(max_length=250,default='')
    #this is list of fields that can be selected 
    #it needs to be returned as an array of field names that can be used to render just these fields in the form for proocol type
    #maybe passed when creation of Listform object 
    FIELD_NAMES = (
    ('forename', 'First name'),
    ('surname', 'Second name'),
    ('yearLevel', 'year level'),
    ('arrivalDate', 'when joining roll'),
    ('leavingDate', 'when leaving roll')
    )
    fields =  models.CharField(max_length=50, choices=FIELD_NAMES,default='')
    
class protocol(models.Model):
    protocolType = models.ForeignKey(protocolType,on_delete=models.DO_NOTHING)
    form = models.OneToOneField(List,on_delete=models.CASCADE)



class task(models.Model): 
    TaskDescription =  models.CharField(max_length=250,default='') 
    protocolType = models.ForeignKey(protocolType,on_delete=models.DO_NOTHING)
    
class taskData(models.Model):
    completed = models.BooleanField(default=False)
    completionDate = models.DateField(null=True)
    notes =  models.CharField(max_length=250,default='')
    protocolLink = models.ForeignKey(protocol,on_delete=models.CASCADE)
    task = models.ForeignKey(task,on_delete=models.CASCADE)

class responsibility(models.Model):
    taskResponsible = models.ForeignKey(task,on_delete=models.CASCADE)
    personResponsible = models.ForeignKey(persons,on_delete=models.CASCADE) 
