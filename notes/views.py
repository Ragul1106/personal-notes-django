from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Note
from django.contrib.auth import login
from .forms import UserRegisterForm

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect("note-list")
    else:
        form = UserRegisterForm()
    return render(request, "registration/register.html", {"form": form})

# List notes
class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = "notes/note_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Note.objects.all()
        return Note.objects.filter(owner=self.request.user)

# View note
class NoteDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Note
    template_name = "notes/note_detail.html"

    def test_func(self):
        note = self.get_object()
        return self.request.user == note.owner or self.request.user.is_superuser

# Create note
class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['title', 'content']
    template_name = "notes/note_form.html"
    success_url = reverse_lazy('note-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# Update note
class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    fields = ['title', 'content']
    template_name = "notes/note_form.html"
    success_url = reverse_lazy('note-list')

    def test_func(self):
        note = self.get_object()
        return self.request.user == note.owner or self.request.user.is_superuser

# Delete note
class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    template_name = "notes/note_confirm_delete.html"
    success_url = reverse_lazy('note-list')

    def test_func(self):
        note = self.get_object()
        return self.request.user == note.owner or self.request.user.is_superuser
