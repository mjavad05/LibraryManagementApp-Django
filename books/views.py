from django.shortcuts import render, redirect
from .models import Book
from .forms import BookForm


# Create your views here.
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})


def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})


def search_books(request):
    query = request.GET.get('q')
    books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    return render(request, 'books/book_list.html', {'books': books})

def filter_books(request):
    price = request.GET.get('price')
    publication_date = request.GET.get('publication_date')
    books = Book.objects.all()

    if price:
        books = books.filter(price__lte=price)
    if publication_date:
        books = books.filter(publication_date__year=publication_date)

    return render(request, 'books/book_list.html', {'books': books})


def edit_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {'form': form})

def delete_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'books/delete_book.html', {'book': book})
