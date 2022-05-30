from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


urlpatterns = [
    path("main/", views.MainView.as_view(), name="main_page"),
    path("add/", views.AddClothView.as_view(), name="add_cloth"),
    path("<slug:slug>/edit", views.EditOfferView.as_view(), name="edit_offer"),
    path("delete/<int:pk>", views.DeleteOfferView.as_view(), name="delete_offer"),
    path("login/", views.LoginPageView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("my_profile/", views.MyProfileView.as_view(), name="my_profile"),
    path("register/", views.RegisterPageView.as_view(), name="register"),
    path("change_password", views.ResetPasswordView.as_view(), name="change_password"),
    path('<slug:slug>/', views.SingleClothView.as_view(), name="single_cloth"),
    path('g/<int:gender>/', views.GenderView.as_view(), name="gender_page"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
