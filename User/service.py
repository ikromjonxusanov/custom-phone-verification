from math import e
from random import sample
from datetime import datetime as d, timedelta as t
from .models import User
from django.contrib.auth import login
def generate_code():
    return sample(range(10**(6-1), 10**6), 1)[0]

def sendCode(request):
    code = generate_code()
    request.session['code'] = code
    request.session['end'] = str(d.now() + t(minutes=2))
    print(code)
    return request

def equalCode(request, c_code):
    code = request.session.get('code', None)
    end = request.session.get('end', None)
    try:
        end = d.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
    except:
        pass
    print(code, end)
    if code and end:
        now = d.now()
        if str(c_code) == str(code):
            del request.session['code']
            del request.session['end']
            return request
        else:
            return False
    return False

def phoneVerfication(request, c_code, phone):
    user = User.objects.get(phone=phone)
    if equalCode(request, c_code):
        user.is_active = True
        user.save()
        login(request, user)
        return request
    return False
    