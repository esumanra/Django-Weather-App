import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm


def home(request):
    weather_data = []
    # url = "https://samples.openweathermap.org/data/2.5/weather?q=London&appid=b6907d289e10d714a6e88b30761fae22"
    url = "https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=75473e364a96f6284851a3bfe3ca592f"
    err_msg = ""
    msg = ""
    msg_class = ""

    if request.method == "POST":
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data["name"].lower().replace(" ", "")
            form.cleaned_data["name"] = new_city
            form.instance.name = new_city

            city_exists = City.objects.filter(name=new_city).count()
            if city_exists:
                err_msg = "City already exists"
            else:
                response = requests.get(url.format(city=new_city), verify=False).json()
                # if city exists, return status is 200
                if response["cod"] != 200:
                    err_msg = "City does not exist"
                else:
                    form.save()

            if not err_msg:
                msg = "City added succesfully"
                msg_class = "is-success"
            else:
                msg = err_msg
                msg_class = "is-danger"

    form = CityForm()
    cities = City.objects.all()
    for city in cities:
        response = requests.get(url.format(city=city), verify=False).json()
        weather = response["weather"][0]
        city_weather = {
            "icon": weather["icon"],
            "name": response["name"],
            "description": weather["description"],
            "temperature": response["main"]["temp"],
            "country": response["sys"]["country"],
        }
        weather_data.append(city_weather)
    return render(
        request,
        "index.html",
        context={
            "weather_data": weather_data,
            "form": form,
            "msg": msg,
            "msg_class": msg_class,
        },
    )


def delete_city(request, city_name):
    print(f"==========delete========={city_name}")
    City.objects.filter(name=city_name.lower()).delete()
    return redirect("home")
