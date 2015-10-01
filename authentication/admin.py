from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from authentication.models import Account, Company, Address

# class AccountAdmin(admin.ModelAdmin):
#   class Meta:
#       model = Account

# admin.site.register(Account, AccountAdmin)

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # password = ReadOnlyPasswordHashField()
    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\"> ---> CLICK HERE <-- .</a>"))

    class Meta:
        model = Account
        fields = ('email', 'password', 'username', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class AccountAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'user_company')
    list_filter = ('optiz', 'user_company',)
    readonly_fields = ('user_created', 'user_updated')
    fieldsets = (
        ('Authorization and Login info', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'tagline', 'lang', 'user_company', 'position',
            'access_level', 'auth_amount', 'user_pic',)}),
        ('Contact info', {'fields': ('street_addr1', 'street_addr2', 'city', 'post_code', 'country', 'phone_main', 'phone_mobile',)}),
        ('Preferences', {'fields': ('request_email', 'offer_email', 'order_email', 'approval_email', 'validated_email',
            'refused_email', 'canceled_email', 'new_user_email', 'info_change_email',)}),
        (None, {'fields': ('user_created_by',  'user_updated_by',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'optiz',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('Authorization and Login info', {'fields': ('email', 'password1', 'password2',)}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'tagline', 'lang', 'user_company', 'position',
            'access_level', 'auth_amount', 'user_pic',)}),
        ('Contact info', {'fields': ('street_addr1', 'street_addr2', 'city', 'post_code', 'country', 'phone_main', 'phone_mobile',)}),
        ('Preferences', {'fields': ('request_email', 'offer_email', 'order_email', 'approval_email', 'validated_email',
            'refused_email', 'canceled_email', 'new_user_email', 'info_change_email',)}),
        (None, {'fields': ('user_created_by',  'user_updated_by',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'optiz',)}),
    )
    search_fields = ('first_name', 'last_name', 'email', 'user_company', 'username',)
    ordering = ('user_company','last_name',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(Account, AccountAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

class AddressAdmin(admin.ModelAdmin):
    class Meta:
        model = Address
    list_display = ('addr_company', 'addr_location', 'addr_type',)
    ordering = ('addr_company',)
    filter_horizontal = ()
    
admin.site.register(Address, AddressAdmin)

class AddressInline(admin.StackedInline):
    model = Address
    extra = 0

class AccountInline(admin.StackedInline):
    model = Account
    extra = 0
    readonly_fields = ('password',)

class CompanyAdmin(admin.ModelAdmin):
    inlines = [
        AddressInline,
        AccountInline,
    ]
    ordering = ['name']
    list_filter = ('name',)
       
admin.site.register(Company, CompanyAdmin)
