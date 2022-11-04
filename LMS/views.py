from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse, JsonResponse
from .models import Books, User, BookIssued, Query
from .barcode import BarCode 
from .news_feed import NewsFeed
from django.core.mail import send_mail


# Create your views here.


def home(request):
    bks = Books.objects.all()
    nf = NewsFeed()
    news = nf.getNews()
    return render(request,"home.html",{'news':news})

def userlogin(request):
    if request.method == 'POST':
        try:
            rn = int(request.POST['rno'])  
            pswd = request.POST['pswd'] 
            user = authenticate(username=rn,password=pswd)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'Incorrect Password or Username')
                return redirect('/login') 
        except: 
            messages.info(request,'Enter Valid Username')
            return redirect('/login')         
    else:
        return render(request,'login.html')

def userlogout(request):
    logout(request) 
    return redirect('home')     
 
def library(request):
    bks = Books.objects.values('title','available')
    if 'search' in request.GET:
        search_val = request.GET.get('search')
        find = Books.objects.filter(title__icontains=search_val)
        print(find.exists())
        if find.exists() and search_val != "":
            return render(request,"library.html",{'find':find})
        else:
            return render(request,'library.html',{'result':"No Result"})                                    
    if 'ssn' in request.GET: 
        ssn = int(request.GET.get('ssn'))
        try :
            issued = BookIssued.objects.get(ssn=ssn)                  
        except:
            issued = None
            book = Books.objects.get(ssn=ssn)
            avail = book.available 
        if issued == None and avail == True:
            id = int(request.GET.get('rno'))
            title = book.title
            user = User.objects.get(roll_no=id)
            user.books += 1
            book.available = False
            issue = str(ssn)
            issues = BookIssued.objects.create(by=id,title=title,ssn=ssn)
            book.save()
            user.save()
            msg = "Book issued " + issue
        else:
            msg = "Book already issued" 
        return HttpResponse(msg)
    if 'opt' in request.GET:
        opt = request.GET.get('opt')
        find = Books.objects.filter(available=opt)
        return render(request,"library.html",{'find':find})
    if 'pdf' in request.GET:
        val = request.GET.get('pdf')
        book = Books.objects.all().values('book_pdf')
        for item in book:
            pdf = item['book_pdf']
            if pdf != '' and val == 'yes':
                find = Books.objects.filter(book_pdf=pdf)
                return render(request,'library.html',{'find':find})      
    return render(request,"library.html",{'bks':bks})      
          
def contact(request): 
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        msg = request.POST['message']

        if name != "" and email != "" and msg != "":
            if not((Query.objects.filter(email__contains = email)).exists()):
                Query.objects.create(full_name=name,email=email,message=msg,status=True)
                messages.info(request, "Query Send by "+ email) 
            else:
                messages.info(request, "Query of " + email + " Already in queue.")
        else:
            messages.info(request, "Name, Email, or Message field is empty")
        return render(request,'contact.html')
    else:
        return render(request,'contact.html')

def test(request):
    if 'name' in request.GET:
        name = request.GET.get('name')
        return HttpResponse(name)
    else:   
        return render(request,'test.html')