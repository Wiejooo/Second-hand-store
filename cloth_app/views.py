from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View, CreateView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, FormView

from cloth_app.forms import ClothesForm, LoginForm, PasswordChangingForm, UserRegisterForm
from cloth_app.models import Clothes


class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        if not self.has_permission():
            return redirect('login')
        return super(UserAccessMixin, self).dispatch(request, *args, **kwargs)


class MainView(View):
    template_name = 'shop/main_page.html'

    def get(self, request):
        return render(request, self.template_name)


class GenderView(ListView):
    model = Clothes
    template_name = 'shop/gender_page.html'
    context_object_name = 'cloth'
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        return Clothes.objects.filter(gender__icontains=self.kwargs.get('gender'))


class AddClothView(UserAccessMixin, FormView):

    raise_exception = False
    permission_required = 'cloth_app.add_clothes'
    permission_denied_message = ''
    login_url = 'main'
    redirect_field_name = 'next'

    template_name = 'shop/form_cloth.html'
    form_class = ClothesForm
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class EditOfferView(UserAccessMixin, UpdateView):

    raise_exception = False
    permission_required = 'cloth_app.change_clothes'
    permission_denied_message = ''
    login_url = 'main'
    redirect_field_name = 'next'

    model = Clothes
    template_name = 'shop/form_cloth.html'
    form_class = ClothesForm
    success_url = reverse_lazy('main_page')


class DeleteOfferView(UserAccessMixin, DeleteView):

    raise_exception = False
    permission_required = 'cloth_app.delete_clothes'
    permission_denied_message = ''
    login_url = 'main'
    redirect_field_name = 'next'

    model = Clothes
    success_url = reverse_lazy('main_page')
    template_name = 'shop/delete.html'


class MyProfileView(ListView):
    model = Clothes
    template_name = 'shop/my_profile.html'

    # def get(self, request):
    #     return render(request, self.template_name)


class RegisterPageView(SuccessMessageMixin, CreateView):
    template_name = 'user/registration.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"


class LoginPageView(View):
    template_name = 'user/login.html'
    form_class = LoginForm

    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('main_page')
        form = self.form_class()
        message = ""
        return render(
            request, self.template_name, context={"form": form, "message": message}
        )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect('main_page')
        message = "Login failed!"
        return render(
            request,
            self.template_name,
            context={"form": form, "message": message},
            status=400,
        )


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main_page')


class ResetPasswordView(View):
    template_name = "user/change_password.html"
    success_url = reverse_lazy("main_page")
    form_class = PasswordChangingForm

    def get(self, request):
        form = self.form_class(User)
        message = ""
        return render(
            request, self.template_name, context={"form": form, "message": message}
        )

    def post(self, request):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("main_page")
        else:
            messages.error(request, "Please correct the error below.")
        form = PasswordChangeForm(request.user)
        return render(request, "shop/main_page.html", {"form": form})


class SingleClothView(DetailView):
    model = Clothes
    template_name = 'shop/single_cloth.html'
    context_object_name = 'cloth'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = Clothes.objects.filter(slug=self.kwargs.get('slug'))
        post.update()

        return context
