"""librarySystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main.views import home , register,viewStocks , stockBooks,login , dashboard , userDashboard , rentBook , myBooks, returnBook,logout
urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , home, name ='index'),
    path('register', register, name='register'),
    path('login', login , name = 'login'),
    path('Librarian/dashboard', dashboard, name='dashboard'),
    path('User/Dashboard', userDashboard , name = 'userDashboard'),
    path('User/Dashboard/rentBook/<int:id>', rentBook, name='rentBook'),
    path('User/Dashboard/myBooks', myBooks , name='myBooks'),
    path('User/Dashboard/returnBook/<int:id>', returnBook , name='returnBook'),
    path('logout', logout , name='logout'),
    path('Librarian/dashboard/StockBooks', stockBooks, name = 'stockBooks'),
    path('Librarian/dashboard/ViewStocks',viewStocks,name='viewStocks')


]
