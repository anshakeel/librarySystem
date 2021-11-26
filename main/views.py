from django.contrib import messages, auth
from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.models import User
from .models import Reader , Librarian , Account , Copy , Book , Stock , Rent
from datetime import date
from datetime import datetime
from django.db.models import Max

from django.contrib.auth.decorators import login_required
def home(request):
    return render(request , "indexMain.html")


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        reg = request.POST.get('register')
        print(first_name,last_name,email,username,password,password1,reg)
        if reg is not None:
            if password == password1:
                if User.objects.filter(username=username).exists():
                    print('username is taken')
                    messages.success(
                        request, "Username is Taken",
                        extra_tags='danger')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    print('Email eixsts')
                    messages.success(
                        request, "Email Already Exists",
                        extra_tags='danger')
                    return redirect('register')
                else:

                    user = User.objects.create_user(username=username, password=password1, email=email,
                                                    first_name=first_name, last_name=last_name)
                    user.save()
                    print('User Created', user)

                    if reg == "1":
                        acc = Account.objects.get(user_id=user)
                        print(acc)
                        sds=Reader(user_id=acc.user_id_id)
                        print("HERE 1", sds)
                        sds.save()

                    elif reg == "2":
                        acc = Account.objects.get(user_id=user)
                        libObj = Librarian(user_id=acc.user_id_id)
                        libObj.save()
                        print("HERE 2", libObj)
                    return redirect('login')
        else:
            messages.success(
                request, "Password not matching",
                extra_tags='danger')
            return redirect('signup')
    else:
        return render(request, 'index.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = auth.authenticate(username=username, password=password)
        if user is not None:

            auth.login(request, user)
            acc = Account.objects.get(user_id=request.user)
            print(acc)
            # s=Reader.objects.get(user_id=acc.id)
            # print(s)
            try:
                Librarian.objects.get(user_id=acc.user_id_id)
                return redirect('dashboard')
            except:
                # Reader.objects.get(user_id=Account.objects.get(user_id=user).user_id_id):
                return redirect('userDashboard')
            # try:
            #     Librarian.objects.get(user_id=acc.user_id_id)
            #     return redirect('dashboard')
            # except:
            #     continue
            # if Librarian.objects.get(user_id=acc.user_id_id):
            #
            # elif Reader.objects.get(user_id=Account.objects.get(user_id=user).user_id_id):
            #     return redirect('userDashboard')
        else:
            messages.success(
                request, "Wrong Username and password",
                extra_tags='danger')
            return render(request,'Login.html')

    return render(request , 'Login.html')
@login_required(login_url="login")
def dashboard(request):
    libUser = Librarian.objects.get(user_id=request.user.id)
    bok = Book.objects.all()
    copies = Copy.objects.all()
    print(libUser)
    res = {
        'lib': libUser,
        'copy': copies,
        'libStat': True,
        'book': bok
    }
    return render(request,'dashboard.html',res)
@login_required(login_url="login")
def userDashboard(request):
    allBooks = Book.objects.all()
    booksSet = {
        'books' : allBooks
    }
    return render(request,'table.html', booksSet)
@login_required(login_url="login")
def rentBook(request , id):
    if request.method == 'POST':
        try:
            Bobj = Copy.objects.filter(isbn_id=id).order_by('-copy_num').first()
            print("checking Stock.....",Bobj.id , Bobj.copy_num)
            bookM = Stock.objects.filter(isbn_id=Bobj.id).latest('stock_date')
            print("Stock Date",bookM.stock_date)
        except:
            messages.success(
                request, "No Stock Available for this Book",
                extra_tags='danger')
            return redirect('userDashboard')
        if Bobj.copy_num != 0:
            date = request.POST['date']
            copy_num = request.POST['copy_num']
            var = str(date).split(' ')
            print("Main date",var[0])
            rentDate=datetime.today().strftime('%Y-%m-%d')
            print(rentDate)
            returnDate = datetime.strptime(var[0],'%m/%d/%Y').strftime('%Y-%m-%d')
            print(rentDate, returnDate , copy_num)
            readObj = Reader.objects.get(user_id=request.user.id)
            Bobj.copy_num -=1
            Bobj.save()
            rentObj = Rent(user_id=request.user.id,isbn=Bobj,
                           copy_num=copy_num,rent_date=rentDate,return_date=returnDate)
            rentObj.save()
            messages.success(
                request, "Successfully Rented " + rentObj.isbn.isbn.title+ " Book",
                extra_tags='success')
            return redirect('userDashboard')
        else:
            messages.success(
                request, "No Extra Copies Available for this Book",
                extra_tags='danger')
            return redirect('userDashboard')
        # Rent(user_id=)
    return redirect('userDashboard')

@login_required(login_url="login")
def myBooks(request):
    getMyBooks = Rent.objects.filter(user_id=request.user.id)
    return render(request , 'myBooks.html', {'rents': getMyBooks})

@login_required(login_url="login")
def returnBook(request, id ):
    obj = get_object_or_404(Rent , pk = id)
    print(obj.isbn.id)
    copyObj = Copy.objects.get(id = obj.isbn.id)
    copyObj.copy_num +=1
    copyObj.save()
    obj.delete()
    messages.success(
        request, "Successfully Returned a Book",
        extra_tags='success')
    return redirect('userDashboard')

def logout(request):
    #user = get_object_or_404(User , pk=id)
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('index')

@login_required(login_url="login")
def stockBooks(request):
    copy_num = request.POST['copy_num']
    copies_id = request.POST.get('copies_id')
    stockDate = datetime.today().strftime('%Y-%m-%d')
    print(copy_num, copies_id , stockDate)
    obj = get_object_or_404(Copy , pk=copies_id)
    obj.copy_num =int(copy_num)
    obj.save()
    libb = Librarian.objects.get(user_id=request.user.id)
    ree = Stock(copy_num=copy_num , isbn=obj , user=libb, stock_date = stockDate)
    ree.save()
    messages.success(
        request, "Stock updated Successfully",
        extra_tags='success')

    return redirect('dashboard')


def viewStocks(request):
    soc = Stock.objects.all().order_by('stock_date')
    return render(request,'ViewStock.html',{'stock': soc})
