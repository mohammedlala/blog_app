from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserCustomForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = UserCustomForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(
                request, f'Account Created For {username}, Now you are able to Login!!')
            return redirect('users-login')

    else:
        u_form = UserRegisterForm()
        p_form = UserCustomForm()

    return render(request, 'users/register.html', {'u_form': u_form, 'p_form': p_form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('users-profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
