from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest
from .models import Author, Book, BookInstance, Genre, Purchase
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AuthorsForm, BookModelInstance, UserRegistrationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact=2).count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    return render(request, 'index.html', context={'num_books': num_books,
                                                  'num_instances': num_instances,
                                                  'num_instances_available': num_instances_available,
                                                  'num_authors': num_authors,
                                                  'num_visits': num_visits
                                                  }, )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 3


class BookDetailView(generic.DetailView):
    model = Book

@login_required
def purchase(request, book_id):
    book = Book.objects.get(id=book_id)
    purchase = Purchase.objects.create(user=request.user, book=book)
    purchase.save()
    return HttpResponseRedirect(reverse('download', args=(book_id,)))

@login_required
def download(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    purchase = Purchase.objects.filter(user=request.user, book=book).first()
    if not purchase:
        return HttpResponseBadRequest("Вы еще не купили эту книгу.")
    file_path = book.file.path
    response = HttpResponse(open(file_path, 'rb').read())
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename=' + book.file.name.split('/')[-1]
    return response

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 3


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail1.html'


class LoanedBooksByUserListView(generic.ListView):
    model = Book
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='2').order_by('due_back')


def authors_add(request):
    author = Author.objects.all()
    authorsform = AuthorsForm()
    paginate_by = 3
    return render(request, "catalog/authors_add.html", {"form": authorsform, "author": author})


def create(request):
    if request.method == "POST":
        author = Author()
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        biographi = request.POST.get("biographi")
        author.save()
        return HttpResponseRedirect("/author_add/")


def delete(request, id):
    try:
        author = Author.objects.get(id=id)
        author.delete()
        return HttpResponseRedirect("/author_add/")
    except:
        return HttpResponseNotFound("<h2>Автор не найден</h2>")


def edit1(request, id):
    author = Author.objects.get(id=id)
    if request.method == "POST":
        author.first_name = request.POST.get("first_name")
        author.last_name = request.POST.get("last_name")
        author.date_of_birth = request.POST.get("date_of_birth")
        author.date_of_death = request.POST.get("date_of_death")
        author.biographi = request.POST.get("biographi")
        author.save()
        return HttpResponseRedirect("/author_add/")
    else:
        return render(request, "catalog/edit1.html", {"author": author})


class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

class book_status(generic.ListView):
    model = Book
    template_name = 'catalog/book_status.html'
    fields = '__all__'
    success_url = reverse_lazy('books')
    paginate_by = 2

def edit_field(request, pk):
    obj = get_object_or_404(BookInstance, pk=pk)
    form = BookModelInstance(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        # redirect to success page
    return render(request, 'catalog/bookinstancechange.html', {'form': form})
