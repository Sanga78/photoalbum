from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from .models import Album,Photo,User,Profile
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse,reverse_lazy
from django.views.generic.edit import FormView
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm,LoginForm,PhotoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout

def index(request):
    return render(request,'index.html') 
def about(request):

    return render(request,'about.html', {'title':'about'})


class HomeView(ListView):
    model = Album
    template_name = 'home.html'
    context_object_name = 'albums'
    ordering = ['-date_created']
    paginate_by = 3
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.exclude(username='admin')  # Add any filtering or ordering if needed
        return context

class UserAlbumListView(ListView):
    model = Album
    template_name = 'user_albums.html'
    context_object_name = 'albums'
    paginate_by = 3
    
    
    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        return Album.objects.filter(user=user).order_by('-date_created')

class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['album_title']
    template_name = 'album_form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user

        # Check if an album with the same title already exists
        existing_album = Album.objects.filter(user=self.request.user, album_title=form.cleaned_data['album_title']).first()

        if existing_album:
            # Display a message to the user
            messages.error(self.request, 'An album with this title already exists.')
            return redirect('album-create')  
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('album-detail', args=[str(self.object.id)])

class AlbumUpdateView(LoginRequiredMixin, UpdateView):
    model = Album
    template_name = 'album_update.html'
    fields = ['album_title']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        album = self.get_object()
        if self.request.user == album.user:
            return True
        return False
    def get_success_url(self):
        return reverse_lazy('album-detail', args=[str(self.object.id)])
            

class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    success_url = '/'
    def test_func(self):
        album = self.get_object()
        if self.request.user == album.user:
            return True
        return False

class AlbumDetailView(DetailView):
    template_name = 'Adetail.html'
    model = Album
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['album_photos'] = Photo.objects.filter(album_id=self.object)
        return context


class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'photo_detail.html'
    context_object_name = 'photo'

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        form = PhotoForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('photo_detail', pk=instance.pk)
        else:
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PhotoForm(instance=self.get_object())
        return context    
    

class AddPhotoView(FormView):
    template_name = 'add_photo.html'
    form_class = PhotoForm

    def form_valid(self, form):
        album_id = self.kwargs['pk']
        album_id = get_object_or_404(Album, pk=album_id)

        photo_title = form.cleaned_data['photo_title']
        image = form.cleaned_data['image']

        Photo.objects.create(album_id=album_id, photo_title=photo_title,image=image)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('album-detail', kwargs={'pk': self.kwargs['pk']})
class UserDetailView(DetailView):
    template_name = 'user_detail.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_albums'] = Album.objects.filter(user=self.object)
        return context
    
def register(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!, You can now login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

class Login(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('album-home')  


def logout_request(request):
    logout(request)
    messages.info(request,"Logged out successfully!")
    return redirect('/')
@login_required 
def profile(request):
    user_profile = Profile.objects.get_or_create(user=request.user)[0]

    if request.method == 'POST':
        u_form= UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, f'You Account has been Updated')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=user_profile)
        u_form= UserUpdateForm(instance=request.user)


    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request, 'users/profile.html', context)