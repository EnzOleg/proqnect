from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import ExpertProfileForm, ExpertSkillFormSet
from .models import Expert
from booking.models import Booking

def experts_search(request):
    query = request.GET.get('q', '')
    if query:
        experts = Expert.objects.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(specialization__icontains=query) |
            Q(bio__icontains=query)
        ).distinct()
    else:
        experts = Expert.objects.all()
    
    context = {
        'query': query,
        'experts': experts,
    }
    return render(request, "experts/experts_search.html", context)


@login_required
def become_expert(request):
    # Если у пользователя уже есть профиль эксперта — редиректим
    if hasattr(request.user, 'expert_profile'):
        return redirect('experts:detail', pk=request.user.expert_profile.id)

    if request.method == 'POST':
        form = ExpertProfileForm(request.POST)
        formset = ExpertSkillFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            # Сохраняем Expert
            expert = form.save(commit=False)
            expert.user = request.user
            expert.save()

            # Привязываем formset к созданному Expert
            skill_forms = formset.save(commit=False)
            for skill_form in skill_forms:
                skill_form.expert = expert
                skill_form.save()

            # Сохраняем роль пользователя
            request.user.role = 'expert'
            request.user.save()

            return redirect('experts:detail', pk=expert.id)
    else:
        form = ExpertProfileForm()
        formset = ExpertSkillFormSet()

    return render(request, 'experts/become_expert.html', {
        'form': form,
        'formset': formset
    })

def expert_detail(request, pk):
    expert = get_object_or_404(Expert, pk=pk)
    return render(request, "experts/expert_detail.html", {"expert": expert})

@login_required
def expert_bookings(request):
    bookings = Booking.objects.filter(expert=request.user)
    return render(request, "experts/expert_dashboard.html", {"bookings": bookings})
