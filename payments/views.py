from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment, User
from .forms import PaymentForm

# Create your views here.
@login_required
def make_payment(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = User.objects.get(pk=request.user.pk)
            payment.save()
            return redirect("payment_history")
    
    else:
        form = PaymentForm()  
    return render(request, "payments/make_payment.html", {"form": form})
    
@login_required
def payment_history(request):
    payments = Payment.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "payments/payment_history.html", {"payments": payments})

