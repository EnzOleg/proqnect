from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .models import Booking
from .forms import BookingRequestForm, ConfirmBookingForm
from experts.models import Expert
from chat.models import Chat

@login_required
def request_booking(request, expert_id):
    expert = get_object_or_404(CustomUser, id=expert_id)
    if request.method == "POST":
        form = BookingRequestForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.expert = expert
            booking.scheduled_time = None  
            booking.status = "pending"
            booking.created_at = now()
            booking.save()
            
            expert_profile = get_object_or_404(Expert, user=expert)
            return redirect('experts:detail', pk=expert_profile.id)

        else:
            return render(request, "booking/request_booking.html", {"form": form, "expert": expert})
    else:
        form = BookingRequestForm()
    return render(request, "booking/request_booking.html", {"form": form, "expert": expert})




@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, expert=request.user)

    if request.method == "POST":
        form = ConfirmBookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.status = "confirmed"
            booking.save()

            user = booking.user
            expert = booking.expert
            chat = (
                Chat.objects
                    .filter(participants=user)
                    .filter(participants=expert)
                    .first()
            )
            if not chat:
                chat = Chat.objects.create()
                chat.participants.add(user, expert)

            return redirect('chat:chat_room', chat_id=chat.id)
    else:
        form = ConfirmBookingForm(instance=booking)
    return render(request, "booking/confirm_booking.html", {"form": form, "booking": booking})

@login_required
def handle_booking(request, booking_id, action):
    booking = get_object_or_404(Booking, id=booking_id, expert=request.user)
    
    if request.method == "POST":
        if action == "decline":
            booking.status = "canceled"
            booking.save()
        elif action == "complete":
            booking.status = "completed"
            booking.save()
        elif action == "delete":
            booking.delete()
            return JsonResponse({"message": "Запись удалена"}, status=200)
        else:
            return JsonResponse({"error": "Недопустимое действие"}, status=400)

        return redirect('booking:my_bookings')
    
    return JsonResponse({"error": "Метод не разрешён"}, status=405)



@login_required
def my_bookings(request):
    incoming_bookings = Booking.objects.filter(expert=request.user).order_by("-created_at")  # Записи К ТЕБЕ
    outgoing_bookings = Booking.objects.filter(user=request.user).order_by("-created_at")  # Записи ОТ ТЕБЯ

    return render(request, "booking/my_bookings.html", {
        "incoming_bookings": incoming_bookings,
        "outgoing_bookings": outgoing_bookings
    })


