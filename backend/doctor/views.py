from django.shortcuts import render
from .models import crop,plant
# Create your views here.

def doctor_home(request):
    plants = plant.objects.all
    if request.method == 'POST':
        search = request.POST['crop']
        plants = plant.objects.filter(crop_name__icontains = search)
        return render(request,'doc.html',{'plants':plants,'search':search})
    else:
        return render(request,'doc.html',{'plants':plants})


def part(request,plant_name):
    return render(request,'cabbage.html',{'plant_name':plant_name})

def disease(request,plant_name,part):
    diseases = crop.objects.filter(crop_name=plant_name,crop_part=part)
    return render(request,'pest.html',{'diseases':diseases})
def info(request,plant_name,part,disease):
    print(plant_name,part,disease)
    final = crop.objects.filter(crop_name=plant_name,crop_part=part,disease_name=disease)
    print(final)
    return render(request,'blog.html',{'final':final})

