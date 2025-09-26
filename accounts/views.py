# accounts/views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
import pyotp, qrcode, io, base64

from .models import UserProfile



def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            #Đảm bảo user có UserProfile
            profile, _ = UserProfile.objects.get_or_create(user=user)

            request.session["pre_2fa_user_id"] = user.id
            return redirect("verify_otp")
    else:
        form = AuthenticationForm(request)
    return render(request, "accounts/login.html", {"form": form})


def verify_otp(request: HttpRequest) -> HttpResponse:
    user_id = request.session.get("pre_2fa_user_id")
    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)

    # Đảm bảo có profile
    profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        code = request.POST.get("otp")
        totp = pyotp.TOTP(profile.otp_secret)
        if totp.verify(code, valid_window=1):
            login(request, user)
            del request.session["pre_2fa_user_id"]
            return redirect("home")
        else:
            return render(request, "accounts/verify_otp.html", {"error": "Mã OTP không hợp lệ"})

    return render(request, "accounts/verify_otp.html")


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            #UserProfile đã được tạo tự động nhờ signal
            profile = user.userprofile
            profile.otp_secret = pyotp.random_base32()
            profile.save()

            #Sinh QR code
            totp = pyotp.TOTP(profile.otp_secret)
            uri = totp.provisioning_uri(name=user.username, issuer_name="San Trao Doi Do Cu")
            qr = qrcode.make(uri)
            buffer = io.BytesIO()
            qr.save(buffer, format="PNG")
            qr_b64 = base64.b64encode(buffer.getvalue()).decode()

            return render(request, "accounts/register_success.html", {"qr_code": qr_b64})
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


    


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    return render(request, "accounts/profile.html", {})


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect("login")  # sau khi logout xong chuyển về trang login


