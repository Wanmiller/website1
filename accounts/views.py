from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm
from .models import LoginAudit, UserProfile


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    lockout_error_message = _("Too many login attempts. Please try again later.")

    def _client_ip(self):
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR", "")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return self.request.META.get("REMOTE_ADDR", "unknown")

    def _normalized_username(self):
        return self.request.POST.get("username", "").strip().lower()

    def _attempts_key(self, username):
        return f"auth:login:attempts:{self._client_ip()}:{username}"

    def _lock_key(self, username):
        return f"auth:login:lock:{self._client_ip()}:{username}"

    def _is_locked(self, username):
        return bool(cache.get(self._lock_key(username)))

    def _register_failed_attempt(self, username):
        attempts_key = self._attempts_key(username)
        lock_key = self._lock_key(username)

        attempts = int(cache.get(attempts_key, 0)) + 1
        cache.set(attempts_key, attempts, settings.LOGIN_LOCKOUT_SECONDS)
        if attempts >= settings.LOGIN_MAX_ATTEMPTS:
            cache.set(lock_key, 1, settings.LOGIN_LOCKOUT_SECONDS)
        return attempts

    def _reset_attempts(self, username):
        cache.delete(self._attempts_key(username))
        cache.delete(self._lock_key(username))

    def post(self, request, *args, **kwargs):
        self._lockout_hit = False
        username = self._normalized_username()
        if username and self._is_locked(username):
            self._lockout_hit = True
            form = self.get_form()
            form.add_error(None, self.lockout_error_message)
            messages.error(request, self.lockout_error_message)
            return self.form_invalid(form)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        username = self._normalized_username()
        if username:
            self._reset_attempts(username)
        response = super().form_valid(form)
        LoginAudit.objects.create(
            user=self.request.user, ip_address=self.request.META.get("REMOTE_ADDR")
        )
        return response

    def form_invalid(self, form):
        if getattr(self, "_lockout_hit", False):
            return super().form_invalid(form)

        username = self._normalized_username()
        if username:
            attempts = self._register_failed_attempt(username)
            if attempts >= settings.LOGIN_MAX_ATTEMPTS:
                messages.error(self.request, self.lockout_error_message)
            else:
                remaining = settings.LOGIN_MAX_ATTEMPTS - attempts
                messages.warning(
                    self.request,
                    _("Invalid credentials. %(remaining)s attempt(s) left.")
                    % {"remaining": remaining},
                )

        return super().form_invalid(form)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _("Registration successful."))
            return redirect("core:home")
        messages.error(request, _("Please correct the errors below."))
    else:
        form = UserRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    profile_obj, _created = UserProfile.objects.get_or_create(user=request.user)
    my_threads = request.user.threads.select_related("person").order_by("-created_at")[:5]
    my_comments = request.user.comments.select_related("thread").order_by("-created_at")[:5]
    my_bookmarks = (
        request.user.bookmarks.select_related("thread", "thread__person").order_by("-created_at")[:5]
    )
    my_ratings = request.user.ratings.select_related("thread").order_by("-updated_at")[:5]
    return render(
        request,
        "accounts/profile.html",
        {
            "profile_obj": profile_obj,
            "my_threads": my_threads,
            "my_comments": my_comments,
            "my_bookmarks": my_bookmarks,
            "my_ratings": my_ratings,
            "breadcrumb_items": [
                {"label": _("Home"), "url": "/"},
                {"label": _("Profile"), "url": None},
            ],
        },
    )


@login_required
def profile_edit(request):
    profile_obj, _created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _("Profile updated."))
            return redirect("accounts:profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile_obj)
    return render(
        request,
        "accounts/profile_edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


def logout_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    logout(request)
    messages.success(request, _("You have been logged out."))
    return redirect("core:home")
