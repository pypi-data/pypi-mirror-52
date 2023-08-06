from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.conf import settings

from .forms import UserChangeForm, UserCreationForm

User = get_user_model()


if settings.DJANGO_SSO_BACKEND_ENABLED or settings.DJANGO_SSO_APP_ENABLED:
    from django_sso_app.core.utils import get_profile_model

    Profile = get_profile_model()

    class ProfileInline(admin.StackedInline):
        model = Profile
        max_num = 1
        can_delete = False


    @admin.register(User)
    class UserAdmin(auth_admin.UserAdmin):
        form = UserChangeForm
        add_form = UserCreationForm

        # pai
        # fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
        fieldsets = auth_admin.UserAdmin.fieldsets
        list_display = ["username", "email", "is_superuser", "sso_id", "sso_rev"]
        search_fields = ["username", "email", "sso_id"]

        # pai
        inlines = [ProfileInline]

else:
    @admin.register(User)
    class UserAdmin(auth_admin.UserAdmin):
        form = UserChangeForm
        add_form = UserCreationForm

        # pai
        # fieldsets = (("User", {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
        fieldsets = auth_admin.UserAdmin.fieldsets
        list_display = ["username", "email", "is_superuser"]
        search_fields = ["username", "email"]

