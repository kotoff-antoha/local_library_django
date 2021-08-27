from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BookInstance, Genre

from django.views import generic

from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# from .models import Author, Book, BookInstance


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_books_find = Book.objects.filter(title__contains='obbi').count()
    num_instances = BookInstance.objects.count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # Метод 'all()' применён по умолчанию.
    num_genres = Genre.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    # del request.session['num_visits']

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_books_find': num_books_find, 'num_genres': num_genres, 'num_visits': num_visits},
    )


# def books(request):
#     num_books = Book.objects.all().count()
#     books_all = Book.objects.all()
#
#     return render(
#         request,
#         'books.html',
#         context={'num_books': num_books, 'books_all': books_all},
#     )


def authors(request):
    num_authors = Author.objects.all().count()
    author_last_name = Author.objects.all()
    # authors_last_name = [author for author in Author]

    return render(
        request,
        'authors.html',
        context={'num_authors': num_authors, 'author_last_name': author_last_name}
    )


class BookListView(generic.ListView):
    model = Book
    # paginate_by = 3


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author


class AuthorDetailView(generic.DetailView):
    model = Author


# def author_info(request,pk):
#     one_author = Author.objects.filter(id__exact=pk)
#     this_author = one_author[0]
#     books_this_author = Book.objects.filter(author__exact=one_author[0])

#     return render(
#         request,
#         'one_author.html',
#         context={'this_author': this_author, 'books_this_author':books_this_author}
#     )

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    # login_url = '/catalog/'

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


from django.contrib.auth.mixins import PermissionRequiredMixin


class AllBorrowedBooksInLibraryListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_see_all_borrower_books'
    template_name = 'catalog/bookinstance_list_all_borrowed_books.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


class AuthorCreate(PermissionRequiredMixin, generic.CreateView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    fields = '__all__'
    initial = {'date_of_death': '12/10/2016', }
    success_url = reverse_lazy('authors')


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    success_url = reverse_lazy('authors')


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    # permission_required = 'catalog.can_mark_returned'
    permission_required = 'catalog.add_book'
    fields = '__all__'
    # initial={'date_of_death':'12/10/2016',}
    success_url = reverse_lazy('books')


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    permission_required = 'catalog.change_book'
    # fields = ['first_name','last_name','date_of_birth','date_of_death']
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = 'catalog.delete_book'
    success_url = reverse_lazy('books')


# class AllBookInstancesListView(generic.ListView):
# model = BookInstance

# def get_queryset(self):
#     return BookInstance.objects.order_by('-book')
# return BookInstance.objects.distinct()

# -------------------------------------------------------
# @permission_required('can_bookinstance_accounting')
def AllBookInstances(request):
    if request.method == 'POST' and request.POST['instance_title'] != 'Show all instances':
        find_instance = str(request.POST['instance_title'])
        all_instance = BookInstance.objects.filter(book__title__exact=find_instance)
        create_select = ['Show all instances']

    elif request.method == 'POST' and request.POST['instance_title'] == 'Show all instances' or not request.method == 'POST':
        all_instance = BookInstance.objects.all()
        list_book_title = []
        for book_inst in all_instance:
            list_book_title.append(book_inst.book.title)
        create_select = sorted(list(set(list_book_title)))


    return render(
        request,
        'bookinstance_list.html',
        context={'bookinstance_list': all_instance, 'create_select': create_select},
    )


class BookInstanceDetailView(generic.DetailView):
    model = BookInstance


class BookInstanceCreate(PermissionRequiredMixin, CreateView):
    model = BookInstance
    # permission_required = 'catalog.can_mark_returned'
    permission_required = 'catalog.add_bookinstance'
    fields = '__all__'
    # initial={'date_of_death':'12/10/2016',}
    success_url = reverse_lazy('all-bookinstances')


class BookInstanceUpdate(PermissionRequiredMixin, UpdateView):
    model = BookInstance
    permission_required = 'catalog.change_bookinstance'
    fields = '__all__'
    success_url = reverse_lazy('all-bookinstances')


class BookInstanceDelete(PermissionRequiredMixin, DeleteView):
    model = BookInstance
    permission_required = 'catalog.delete_bookinstance'
    success_url = reverse_lazy('all-bookinstances')



