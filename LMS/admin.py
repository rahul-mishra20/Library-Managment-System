from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Books, User, BookIssued, Query
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
import datetime as dt


 #Register your models here.

admin.site.site_header = "Library Administration"
admin.site.index_title = "Library Database"

admin.site.disable_action('delete_selected')

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('roll_no', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password',  'admin')

    def clean_password(self):
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('roll_no','email','full_name','parent_name','parent_no','books','mob_no', 'admin')
    list_filter = ('admin','faculty','student')
    fieldsets = (
        ('User Information', {'fields': ('roll_no','email','full_name','parent_name','parent_no','books','mob_no', 'password')}),
        ('User Permissions', {'fields': ('admin','student','faculty')}),
    )

    add_fieldsets = (
        ('User Information', {
            'classes': ('wide',),
            'fields': ('roll_no','email','full_name','parent_name','parent_no','books','mob_no','password1', 'password2')}),
            ('User Permissions', {'fields': ('admin','student','faculty')}),
    )
    search_fields = ('roll_no',)
    ordering = ('roll_no',)
    filter_horizontal = ()
    search_fields =['roll_no','full_name']

    actions = ['delete_selected']

class BookAdmin(admin.ModelAdmin):
    list_display = ['title','ssn','available']
    search_fields = ['title', 'ssn']
    actions = ['delete_selected']

class QueryAdmin(admin.ModelAdmin):
    list_display = ['full_name','email','status']
    search_fields = ['full_name','email']
    actions = ['delete_selected']

def return_book(modeladmin, request, queryset):
    users = queryset.values('by','ssn')
    for i in users:
        id = i['by']
        ssn = i['ssn']
        try:
            item = User.objects.get(roll_no=id)
            book = Books.objects.get(ssn=ssn)
            item.books -= 1
            book.available = True
            queryset.delete()
            item.save()
            book.save()            
        except:
            print("Some error occured bro")        

return_book.short_description = "Return Book"

def issue_book(modeladmin,request,queryset):
    users = queryset.values('ssn')
    for item in users:
        ssn = item['ssn']
        try:
            book = BookIssued.objects.get(ssn=ssn)
            issue_date = dt.datetime.now()
            return_date = issue_date + dt.timedelta(days=15)
            book.issue_date = issue_date
            book.return_date = return_date
            book.save()
        except:
            print("Some error occured bro")     

issue_book.short_description = "Issue Book"


class BookIssuedAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['by','title','ssn','issue_date','return_date']
    actions = [return_book,issue_book]
    search_fields = ['by','ssn']

    def has_add_permission(self, request):
        return False


admin.site.register(User,UserAdmin)
admin.site.register(Books,BookAdmin)
admin.site.register(BookIssued,BookIssuedAdmin)
admin.site.register(Query, QueryAdmin)
admin.site.unregister(Group)


# beautifulsoup4    (4.8.2)
# Django            (3.0.4 ) 
# feedparser        (5.2.1)
# opencv-python     (4.2.0.32)
# pip               (20.0.2)
# pytz              (2019.3)
# pyzbar            (0.1.8)
# pillow
# psycopg2