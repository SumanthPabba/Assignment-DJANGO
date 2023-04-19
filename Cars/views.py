from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Cars.models import Profile
from Cars.forms import CarDetailsForm
from django.contrib import messages
from .models import Cars, otherDetails
from rest_framework import filters
from datetime import datetime
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from .serializers import CarSerializer
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.models import User 


# Create your views here.

def base(request):

    return render(request, 'cars/base.html')


@login_required
def index(request):

    return render(request, 'cars/index.html')

@login_required
def addcar(request):

    if request.method == 'POST':
        form = CarDetailsForm(request.POST)
        if form.is_valid():
            dealer_name = form.cleaned_data.get('dealerName')
            if dealer_name.user.profile.role == 'Dealer':
                form.save()
                messages.success(request, f"Car {Cars.objects.order_by('-id')[0]} added!")
                return redirect('available')
            else:
                messages.warning(request, 'You are not authorized to add cars')

    else:
        form = CarDetailsForm()
    return render(request, 'cars/cardetails.html', {'form':form})

@login_required
def updateCar(request, id):
    car = Cars.objects.filter(id=id).first()
    
    if car.dealerName == request.user.profile:
        if request.method == "POST":
            
            carName = request.POST['CarName']
            modelName = request.POST['ModelName']
            carNumber = request.POST['CarNumber']
            features = request.POST.get('Features', "Guest (or whatever)")
            isAvailable =request.POST['IsAvailable']
            fuelconsumption = request.POST['fuelConsumption']
            carinsurance = request.POST['carInsurance']
            costPerDay = request.POST['CostPerDay']
    
            car.CarName = carName
            car.ModelName = modelName
            car.CarNumber = carNumber
            car.Features = features
            car.IsAvailable = isAvailable
            car.fuelConsumption = fuelconsumption
            car.carInsurance = carinsurance
            car.CostPerDay = costPerDay
            car.save()
    
            try:
                image = request.FILES['image']
                car.CarImage = image
                car.save()
            except:
                pass
            return redirect('available')
        return render(request, "cars/update.html", context={"car":car})
    else:
        messages.warning(request, "you are not dealer for this car")
        return redirect("available")



@login_required
def delete(request, id):

    car = Cars.objects.get(id=id)
    if car.dealerName == request.user.profile:
        car = Cars.objects.get(id=id)
        car.delete()
        messages.success(request, "Successfully deleted")
        return redirect('available')
    else:
        messages.warning(request, "You were not allowed to delete this car")
        return redirect("available")


# @method_decorator(login_required, name='dispatch')
# class Available(TemplateView): 

#     template_name = "cars/available.html"
#     def get_context_data(self, request, **kwargs):

#         context = super().get_context_data(**kwargs)
#         context['cars'] = Cars.objects.all()
#         p = Paginator(context, 3)
#         page_number=request.GET.get('page')
#         page_obj = p.get_page(page_number)
#         return context


@login_required
def available(request):
    
    cars = Cars.objects.all()
    p = Paginator(cars, 2)
    page_number=request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request, "cars/available.html", context={'cars':page_obj})

@login_required
def get_image(pid, request):
    return render(request, 'disp.html', {'img' : pid})

@method_decorator(login_required, name='dispatch')
class search(TemplateView):
    template_name = 'cars/available.html'
    model = Cars

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        car_name = self.request.GET['query']
        context['cars'] = Cars.objects.filter(CarName__icontains = car_name)
        return context

 
@login_required()
def book(request,id):
    
    car_details = Cars.objects.filter(id=id).first()
    if request.method == 'POST':

        username = request.user.profile.username
        phonenumber = request.POST['phone_number']
        Address = request.POST['address']
        fromdate = request.POST['from_date']
        todate = request.POST['to_date']    
        username = Profile.objects.get(username=username)
        book_details = Cars.objects.create(username=username, phone_number=phonenumber, address=Address, from_date=fromdate, to_date=todate)
        book_details.save()
        d1 = datetime.strptime(request.POST['from_date'], "%Y-%m-%d")
        d2 = datetime.strptime(request.POST['to_date'], "%Y-%m-%d")
        delta = (d2-d1).days
        
        Cars.objects.filter(id=id).update(IsAvailable="No")
        subject = "Booked a car"
        email_template_name = "cars/book_email.txt"
        c = {"name":request.user.profile.username,
        "email": request.user.email,
        "carName" : car_details.CarName,
        "carNumber": car_details.CarNumber,
        "fromdate" : fromdate,
        "todate" : todate,
        "noofdays" : delta,
        "Fare": (car_details.CostPerDay) * delta,
        'domain':'127.0.0.1:8000',
        'site_name': 'Website',
        "uid": urlsafe_base64_encode(force_bytes(request.user.pk)),
        "user": request.user,
        'token': default_token_generator.make_token(request.user),
        'protocol': 'http',
        }
        email = render_to_string(email_template_name, c)
        try:
            send_mail(subject, email, 'sunnycool1811@gmail.com' , [request.user.email], fail_silently=False)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return render(request, "cars/thank.html")
    return render(request, "cars/book.html", {'car_details':car_details})


@login_required
def orders_list(request):
    user = User.objects.filter(username = request.user.username)
    profile = Profile.objects.filter(email=user.email)
    orders = otherDetails.objects.filter(username=profile.username)
    print(orders)
    return render(request, 'cars/orders.html', {'orders': orders})

