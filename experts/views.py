from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from .forms import ExpertProfileForm, ExpertSkillFormSet, ReviewForm
from .models import Expert, Review
from booking.models import Booking

RUS_TO_ENG = {
    "разработчик": "developer",
    "дизайнер": "designer",
    "маркетинг": "marketing",
    "финансы": "finance",
    "киберспорт": "cybersport",
    "другое": "other"
}

def find_matching_specialization(query):
    query = query.lower()
    for rus_name, eng_code in RUS_TO_ENG.items():
        if rus_name.startswith(query):
            return eng_code
    return None

def experts_search(request):
    query = request.GET.get('q', '').strip().lower()
    specialization_match = find_matching_specialization(query)

    if query:
        filters = Q(user__first_name__icontains=query) | \
                  Q(user__last_name__icontains=query) | \
                  Q(bio__icontains=query) | \
                  Q(custom_specialization__icontains=query)

        if specialization_match:
            filters |= Q(specialization=specialization_match)

        experts = Expert.objects.filter(filters).distinct()
    else:
        experts = Expert.objects.all()

    context = {
        'query': query,
        'experts': experts,
    }
    return render(request, "experts/experts_search.html", context)



@login_required
def become_expert(request):
    if hasattr(request.user, 'expert_profile'):
        return redirect('experts:detail', pk=request.user.expert_profile.id)

    if request.method == 'POST':
        form = ExpertProfileForm(request.POST)
        formset = ExpertSkillFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            expert = form.save(commit=False)
            expert.user = request.user
            expert.save()

            skill_forms = formset.save(commit=False)
            for skill_form in skill_forms:
                skill_form.expert = expert
                skill_form.save()

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


@login_required
def add_review(request, expert_id):
    expert = get_object_or_404(Expert, pk=expert_id)
    if not Booking.objects.filter(user=request.user, expert=expert.user, status="completed").exists():
        return HttpResponseForbidden("Нельзя оставить отзыв без завершенной консультации!")
    form = ReviewForm(request.POST or None)
    if form.is_valid():
        rev = form.save(commit=False)
        rev.reviewer = request.user
        rev.expert = expert
        rev.save()
        update_expert_rating(expert)
        return redirect("experts:detail", pk=expert_id)
    return render(request, "experts/add_review.html", {"form": form, "expert": expert})
    

def update_expert_rating(expert):
    reviews = Review.objects.filter(expert=expert)
    
    if reviews.exists():
        total_rating = sum(review.rating for review in reviews)
        review_count = reviews.count()
        expert.rating = total_rating / review_count
        print(f"New rating for expert {expert.id}: {expert.rating}")
    else:
        expert.rating = 0  
    
    expert.save()
