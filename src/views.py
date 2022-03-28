from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt 

import razorpay


from .models import Coffee
# Create your views here.
def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = int(request.POST.get("amount"))*100
        client = razorpay.Client(auth=("rzp_test_b8FE4yq6XB6FGB","b41W2p9AkoDfzzE5p5aM1GSE"))
        payment= client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
        print(payment)
        coffee = Coffee(name=name,amount=amount,payment_id=payment['id'])
        coffee.save()
        return render(request,'index.html',{'payment':payment})
    return render(request,'index.html')
    

@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        data = {}
        for key,val in a.items():
            if key == "razorpay_order_id":
                data["razorpay_order_id"] = val
                order_id = val
            elif key == "razorpay_payment_id":
                data["razorpay_payment_id"] = val
            elif key == "razorpay_signature":
                data["razorpay_signature"] = val

        user = Coffee.objects.filter(payment_id=order_id).first()
        
        user.save()
        client = razorpay.Client(auth=("rzp_test_b8FE4yq6XB6FGB","b41W2p9AkoDfzzE5p5aM1GSE"))
        check = client.utility.verify_payment_signature(data)
        if check:
            return render(request,'error.html')
        user.paid = True
        user.save()
        print(check)
    return render(request,'success.html')