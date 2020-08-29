from django.urls import path

from applications.onboarding import views
from applications.onboarding.apps import OnboardingConfig

app_name = OnboardingConfig.label

urlpatterns = [
    path("profile-update/", views.ProfileUpdateView.as_view(), name="profile-update"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("sign-in/", views.SignInView.as_view(), name="sign-in"),
    path("sign-out/", views.SignOutView.as_view(), name="sign-out"),
    path("sign-up/", views.SignUpView.as_view(), name="sign-up"),
]
