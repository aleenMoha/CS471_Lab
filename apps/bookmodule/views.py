from .models import Book
from django.shortcuts import render

def index(request): 
    name = request.GET.get("name") or "world!"
    return render(request, "bookmodule/index.html" , {"name": name})

def index2(request, val1 = 0):   #add the view function (index2)
    return HttpResponse("value1 = "+str(val1))

def viewbook(request, bookId):
    # assume that we have the following books somewhere (e.g. database)
    book1 = {'id':123, 'title':'Continuous Delivery', 'author':'J. Humble and D. Farley'}
    book2 = {'id':456, 'title':'Secrets of Reverse Engineering', 'author':'E. Eilam'}
    targetBook = None
    if book1['id'] == bookId: targetBook = book1
    if book2['id'] == bookId: targetBook = book2
    context = {'book':targetBook} # book is the variable name accessible by the template
    return render(request, 'bookmodule/show.html', context)

def index(request):
    return render(request, "bookmodule/index.html")
 
def list_books(request):
    return render(request, 'bookmodule/list_books.html')
 
def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')
 
def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')

def links(request):
    return render(request, "bookmodule/links.html")

def formatting(request):
    return render(request, "bookmodule/formatting.html")

def listing(request):
    return render(request, "bookmodule/listing.html")

def tables(request):
    return render(request, "bookmodule/tables.html")

def search(request):
    if request.method == "POST":
        string = request.POST.get('keyword', '').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')

        books = __getBooksList()
        newBooks = []

        for item in books:
            contained = False

            if isTitle and string in item['title'].lower():
                contained = True

            if not contained and isAuthor and string in item['author'].lower():
                contained = True

            if contained:
                newBooks.append(item)

        return render(request, 'bookmodule/bookList.html', {'books': newBooks})

    return render(request, 'bookmodule/search.html')
    

def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]

def construct(request):
    mybook = Book(title = 'Continuous Delivery', author = 'J.Humble and D. Farley', edition = 1).save
    mybook = Book.objects.create(title = 'Continuous Delivery', author = 'J.Humble and D. Farley', edition = 1).save

def simple_query(request):
    construct(request)
    mybooks=Book.objects.filter(title__icontains='and') # <- multiple objects
    return render(request, 'bookmodule/bookList.html', {'books':mybooks})

def complex_query(request):
    mybooks=books=Book.objects.filter(author__isnull = False).filter(title__icontains='and')[:10]
    if len(mybooks)>=1:
        return render(request, 'bookmodule/bookList.html', {'books':mybooks})
    else:
        return render(request, 'bookmodule/index.html')

from django.shortcuts import render
from django.db.models import Q, Count, Sum, Avg, Max, Min
from .models import Book


def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/lab8/task1.html', {'books': books})


def lab8_task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) &
        (Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/lab8/task2.html', {'books': books})


def lab8_task3(request):
    books = Book.objects.filter(
        ~Q(edition__gt=3) &
        ~(Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/lab8/task3.html', {'books': books})


def lab8_task4(request):
    books = Book.objects.all().order_by('title')
    return render(request, 'bookmodule/lab8/task4.html', {'books': books})


def lab8_task5(request):
    stats = Book.objects.aggregate(
        num_books=Count('id'),
        total_price=Sum('price'),
        avg_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price')
    )
    return render(request, 'bookmodule/lab8/task5.html', {'stats': stats})


from django.shortcuts import render
from django.db.models import (
    Sum, Count, Avg, Min, Max, F, FloatField, ExpressionWrapper, Q
)
from .models import Book2, Publisher

def lab9_task1(request):
    total_stock = Book2.objects.aggregate(total=Sum('quantity'))['total'] or 1

    books = Book2.objects.annotate(
        availability_percentage=ExpressionWrapper(
            (F('quantity') * 100.0) / total_stock,
            output_field=FloatField()
        )
    )

    context = {
        'books': books,
        'total_stock': total_stock
    }
    return render(request, 'bookmodule/lab9/task1.html', context)

def lab9_task2(request):
    publishers = Publisher.objects.annotate(
        total_book_stock=Sum('book2__quantity')
    )

    context = {'publishers': publishers}
    return render(request, 'bookmodule/lab9/task2.html', context)


def lab9_task3(request):
    publishers = Publisher.objects.annotate(
        oldest_book_date=Min('book2__pubdate')
    )

    return render(request, 'bookmodule/lab9/task3.html', {
        'publishers': publishers
    })

def lab9_task4(request):
    publishers = Publisher.objects.annotate(
        avg_price=Avg('book2__price'),
        min_price=Min('book2__price'),
        max_price=Max('book2__price')
    )

    context = {'publishers': publishers}
    return render(request, 'bookmodule/lab9/task4.html', context)

def lab9_task5(request):
    publishers = Publisher.objects.annotate(
        high_rated_books_count=Count('book2', filter=Q(book2__rating__gte=4))
    )

    context = {'publishers': publishers}
    return render(request, 'bookmodule/lab9/task5.html', context)

def lab9_task6(request):
    publishers = Publisher.objects.annotate(
        filtered_books_count=Count(
            'book2',
            filter=Q(book2__price__gt=50, book2__quantity__lt=5, book2__quantity__gte=1)
        )
    )

    context = {'publishers': publishers}
    return render(request, 'bookmodule/lab9/task6.html', context)


