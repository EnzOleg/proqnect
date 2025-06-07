from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment, User, Balance
from .forms import PaymentForm
from decimal import Decimal

# Create your views here.
@login_required
def make_payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = User.objects.get(pk=request.user.pk)
            payment.save()
            return redirect("payments/payment_history")
    
    else:
        form = PaymentForm()  
    return render(request, "payments/make_payment.html", {"form": form})
    
@login_required
def add_balance(request, amount):
    if request.method == "POST":
        balance_obj, created = Balance.objects.get_or_create(user=request.user)
        balance_obj.balance += Decimal(amount)
        balance_obj.save()
        return redirect("payments/payment_history")  
    return render("payments/add_balance")

def withdraw_balance(request, amount):
    balance_obj, created = Balance.objects.get_or_create(user=request.user)
    balance_obj.balance -= Decimal(amount)
    balance_obj.save()
    return redirect("payment_history") 

@login_required
def payment_history(request):
    payments = Payment.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "payments/payment_history.html", {"payments": payments})

