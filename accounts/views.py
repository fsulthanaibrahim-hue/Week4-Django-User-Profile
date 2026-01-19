from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib.auth import login
from .forms import SignupForm
from django.http import JsonResponse
from .models import Profile

def home_view(request):
    return render(request, 'accounts/home.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        if "delete_avatar" in request.POST:
            profile.avatar.delete(save=True)
            return redirect("profile")
        
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            return redirect("profile")   # redirect after save

    else:
        form = ProfileForm(instance=profile)

    return render(request, "accounts/profile.html", {
        "form": form,
        "profile": profile
    })



def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('profile')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


@login_required
def delete_avatar(request):
    if request.method == 'POST':
        profile = request.user.profile
        if profile.avatar:
            profile.avatar.delete(save=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)    


