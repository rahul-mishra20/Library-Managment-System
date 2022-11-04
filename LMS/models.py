from django.db import models
from django.contrib.auth.models import AbstractBaseUser ,BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,roll_no,email,full_name,parent_name,parent_no,mob_no,password=None,is_admin=False,is_staff=False,is_student=False):
        if not roll_no:
            raise ValueError("User must have a Roll Number/ID.")
        if not password:
            raise ValueError("User must have a password.")
        if not email:
            raise ValueError("User must have a email.")
        if not full_name:
            raise ValueError("User must have a Name.")
        if not parent_name:
            raise ValueError("User must have a Parent Name.")
        if not parent_no:
            raise ValueError("User must have a Parent Number.")
        if not mob_no:
            raise ValueError("User must have a Mobile Number")
        user = self.model(roll_no=roll_no,email=email,full_name=full_name,parent_name=parent_name,parent_no=parent_no
                         ,mob_no=mob_no)               #
        user.set_password(password)
        user.admin = is_admin
        user.faculty = is_staff
        user.student = is_student
        user.save(using=self._db)
        return user
    def create_superuser(self,roll_no,email,full_name,parent_name,parent_no,mob_no,password=None):
        user = self.create_user(roll_no,email,full_name,parent_name,parent_no,mob_no,password=password,is_admin=True,is_staff=True)
        return user
    def create_faculty(self,roll_no,email,full_name,parent_name,parent_no,mob_no,password=None):
        user = self.create_user(roll_no,email,full_name,parent_name,parent_no,mob_no,password=password,is_staff=True)
        return user  
    def create_student(self,roll_no,email,full_name,parent_name,parent_no,mob_no,password=None):
        user = self.create_user(roll_no,email,full_name,parent_name,parent_no,mob_no,password=password,is_student=True)
        return user         

   
class User(AbstractBaseUser):
    full_name = models.CharField(max_length=255)
    roll_no = models.BigIntegerField( unique=True,primary_key=True)
    mob_no = models.BigIntegerField( unique=True)
    email = models.EmailField(max_length=255, unique=True)
    parent_name = models.CharField(max_length=255)
    parent_no = models.BigIntegerField( unique=True)
    admin = models.BooleanField(default=False)
    student = models.BooleanField(default=False)
    faculty = models.BooleanField(default=False)
    books = models.IntegerField(validators=[MaxValueValidator(3),MinValueValidator(0)],default=0)

    USERNAME_FIELD = 'roll_no'
    REQUIRED_FIELDS =['full_name','email','parent_name','parent_no','mob_no']

    objects = UserManager()

    def __str__(self):
        return self.full_name
    def has_perm(self,perm,object=None):    
        return True
    def has_module_perms(self,app_label):
        return True      

    @property
    def is_staff(self):
        return self.faculty    
    @property
    def is_admin(self):
        return self.admin   
    @property
    def is_student(self):
        return self.student 
                 
                 
class Books(models.Model):
    title = models.CharField(max_length=50)
    ssn = models.BigIntegerField(unique=True,primary_key=True)
    barcode = models.BigIntegerField(default=1)
    author = models.CharField(max_length=50)
    available = models.BooleanField(default=False)
    img = models.ImageField(upload_to='cover')
    book_pdf = models.FileField(upload_to='books_pdf',null=True, blank=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Books'


class BookIssued(models.Model):
    by = models.BigIntegerField()
    title = models.CharField(max_length=50)
    ssn = models.BigIntegerField(unique=True,primary_key=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = 'Book Issued'


class Query(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name
    class Meta:
        verbose_name_plural = "Queries"

