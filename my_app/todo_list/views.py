from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect
# module to read string from entity list as class name
import sys



def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

# Create your views here.
def home(request):

    if request.method == 'POST':
        form = ListForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,('Item added to list'))
            
    all_items = List.objects.all
    people = persons.objects.all
    protocoltypeObjects = protocoltype.objects.all
    
    return render(request,'home.html',{'all_items' : all_items,'people' : people,'protocoltype':protocoltypeObjects})

def protocolAdd(request,type):
    typeObject = protocoltype.objects.get(pk=type) 

    if request.method == 'POST':
        form = ListForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request,('Protocol created'))
            return redirect('home')
    else: 
        newProtocol = protocol()
        newProtocol.type = typeObject 
        form = ListForm(instance=newProtocol)
        visible_fields = newProtocol.visibleFields()
        invisible_fields = []
        for field in form.fields:
            if field not in visible_fields:
                invisible_fields.append(field)
        for field in invisible_fields:
            if field in form.fields:
                form.fields.pop(field)
    #set filter attribute from list of fields in type object
        protocoltypeName = typeObject.protocolTypeName
        return render(request,'protocolAdd.html',{'form' : form, 'protocoltype' : protocoltypeName})

# orders items alphabetically
def order(request):    
    # order items (minus sign for descending order) use eg [:5] at end of line to limit items returned
    people = persons.objects.all
    all_items = List.objects.order_by('item')
    
    return render(request,'home.html',{'all_items' : all_items,'people' : people})


def filter(request,query):
    people = persons.objects.all

    # filters across models using name of manaytomanyfield then attribute in related model, separated by __
    filtered_items = List.objects.filter(people__name = query)

    if len(filtered_items) > 0:
        messages.success(request,('Filtered by '+query))  
    elif query == "all":
        filtered_items = List.objects.all()
        messages.success(request,('All items'))  
    else:
        messages.success(request,('No filtered items')) 

    return render(request,'home.html',{'all_items' : filtered_items,'people' : people})   

def about(request):
    my_name ="Nick"
    return render(request,'about.html',{'name' : my_name})

def delete(request, list_id):
    item = List.objects.get(pk=list_id)
    item.delete()
    messages.success(request,('Item deleted'))
    return redirect('home')

def cross_off(request, list_id):
    item = List.objects.get(pk=list_id)
    item.completed = True
    item.save()
    return redirect('home')

def uncross(request, list_id):
    item = List.objects.get(pk=list_id)
    item.completed = False
    item.save()
    return redirect('home')

#view for editing or adding items
def edit(request,list_id):
    
#if request received from edit form submission
    if request.method == 'POST':
        #checks if form submission is from pre-existing item on list
        try:
            item = List.objects.get(pk=list_id)        
            form = ListForm(request.POST or None, instance=item)
            message="Item edited"
        #if is new item
        except:
            form = ListForm(request.POST or None)
            message="Item added"
            
        if form.is_valid():
            form.save()    
        
        #if form invalid
        else:
            message = 'Invalid form'

        messages.success(request,(message))
        return redirect('home')

#if request received from edit icon by item on home page list or add button
    else:
        #if item on list
        if list_id != '0':
            item = List.objects.get(pk=list_id)
            form = ListForm(request.POST or None, instance=item)
            return render(request,'edit.html',{'form' : form, 'item' : item})
        #if request received from 'add' button on home page (passes id as 0)
        else:
            form = ListForm()
            return render(request,'edit.html',{'form' : form})


#view for editing or adding records in entities (eg persons, protocol types, tasks) 
# (this is very simliar code to def edit and so should be way to pass parameter to def than determines which form is run)
def entityForm(request,list_id,modelName):
    
#if request received from edit form submission
    if request.method == 'POST':
        #checks if form submission is from pre-existing record in model
        if modelName == 'persons':
            if list_id and list_id != "noId":
                item = persons.objects.get(pk=list_id)        
                form = personsForm(request.POST or None, instance=item)
                message="Person edited"
            #if is new item
            else:
                form = personsForm(request.POST or None)
                message="Person added"
            model = persons.objects.all

        elif modelName == 'protocoltype' or modelName == 'Protocol type':
            if list_id and list_id != "noId":
                item = protocoltype.objects.get(pk=list_id)        
                form = protocolTypeForm(request.POST or None, instance=item)
                message="protocl type edited"
            #if is new item
            else:
                form = protocolTypeForm(request.POST or None)
                message="protocol type added"
            model = protocoltype.objects.all

        elif modelName == 'task' or modelName == 'tasks':
            if list_id and list_id != "noId":
                item = task.objects.get(pk=list_id)        
                form = taskForm(request.POST or None, instance=item)
                message="task edited"
            #if is new item
            else:
                form = taskForm(request.POST or None)
                message="task added"
            model = task.objects.all
            
        if form.is_valid():
            form.save()    
        
        #if form invalid
        else:
            errors = form.errors
            message = errors

        messages.success(request,(message))
        return render(request,'entities.html',{'model' : model,'modelName':modelName})

#if request received from entity page
    else:
        #if from item on list finds object instance and returns model appropriate form
        item=""
        if list_id != 'noId':
            model = str_to_class(modelName)
            item = model.objects.get(pk=list_id)
            if modelName == 'persons':
                form = personsForm(request.POST or None, instance=item)
            elif modelName == 'Protocol type' or modelName == 'protocoltype':
                form = protocolTypeForm(request.POST or None, instance=item)
                
            elif modelName == 'task' or modelName == 'tasks':
                form = taskForm(request.POST or None, instance=item)   
        #if request received from 'add' button on entity page (passes id as 0)
        else:   
            if modelName == 'persons':
                form = personsForm(request.POST or None)
            elif modelName == 'Protocol type' or modelName == 'protocoltype':
                form = protocolTypeForm(request.POST or None)
            elif modelName == 'task' or modelName == 'tasks':
                form = taskForm(request.POST or None)
            else:
                form = taskForm(request.POST or None)
        
        return render(request,'edit.html',{'form' : form, 'item' : item})

def entities(request,modelName):
    if modelName == 'persons':
        model = persons.objects.all
    elif modelName == 'Protocol type':
        model = protocoltype.objects.all
    elif modelName == 'tasks':
        model = task.objects.all
    else:
        model = persons.objects.all
    return render(request,'entities.html',{'model' : model,'modelName':modelName})

def deleteInstance(request, list_id,modelName):
    
    if modelName == 'persons':
        item = persons.objects.get(pk=list_id)
        model = persons.objects.all
    elif modelName == 'protocoltype':
        item = protocoltype.objects.get(pk=list_id)
        model = protocoltype.objects.all
    elif modelName == 'task':
        item = task.objects.get(pk=list_id)
        model = task.objects.all 
    item.delete()
    messages.success(request,(modelName +' deleted'))
    return render(request,'entities.html',{'model' : model,'modelName':modelName})