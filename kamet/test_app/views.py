from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    CreateView,
    TemplateView,
    View,
)
from . import models
from . import forms

# Create your views here.
class AdminPanel(ListView):
    template_name = "admin_base.html"
    model = models.TestUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Users & Submissions'
        context['table'] = 'table table-striped'
        context['header'] = [('Users','pass'),('Questions Attempted', 'text-end')]
        context['svg'] = [('svgs/sliders.svg','edit_user')]
        context['link'] = 'questions'
        context['addr'] = 'add_user'
        return context
    
class Topics(ListView):
    template_name = "admin_base.html"
    model = models.Topics
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = 'active'
        context['title'] = 'All Topics'
        context['table'] = 'table table-striped table-bordered'
        context['header'] = [('Topic','pass'),('Number of questions', 'text-end')]
        context['svg'] = [('svgs/pencil-square.svg',"edit_topic",''),('svgs/trash-fill.svg','','data-mdb-ripple-init data-mdb-modal-init')]
        context['link'] = 'questions'
        context['addr'] = 'add_topic'
        return context

class AddTopic(CreateView):
    template_name = 'add.html'
    form_class = forms.TopicForm
    success_url = 'topics'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = 'active'
        context['title'] = 'Add a new Topic'
        return context
    
class DelTopic(DeleteView):
    model = models.Topics
    template_name = None
    success_url = reverse_lazy("topics")
    
class UpdateTopic(UpdateView):
    model = models.Topics
    template_name = 'add.html'
    form_class = forms.TopicForm
    success_url = reverse_lazy("topics")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = 'active'
        context['title'] = 'Edit Topic'
        return context

class AddUser(CreateView):
    template_name = 'add.html'
    form_class = forms.UserForm
    success_url = reverse_lazy('index')
    
    def form_valid(self, form: BaseModelForm):
        self.object = form.save()
        tu = models.TestUser.objects.create(user = self.object, attempts=form.cleaned_data['attempts'])
        #tu.send_email(orm.cleaned_data['password'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add a new User'
        return context
    
class UpdateUser(UpdateView):
    model = models.TestUser
    template_name = 'add.html'
    form_class = forms.UpdateUserForm
    success_url = reverse_lazy("index")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit User'
        return context
    
class TopicQuestions(ListView):
    template_name = "list.html"
    model = models.Question
    
    def get_queryset(self):
        return self.model.objects.filter(topics=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Questions for'
        context['topics'] = models.Topics.objects.get(id=self.kwargs['pk'])
        context['addr'] = 'add_question'

        return context
    
class AddQuestion(CreateView):
    template_name = 'add.html'
    form_class = forms.QuestionForm
    success_url = reverse_lazy('topics')
    
    def form_valid(self, form: BaseModelForm):
        print(self.kwargs['pk'])
        form.instance.topics = models.Topics.objects.get(id=self.kwargs['pk'])
        # Call the parent class's form_valid method to save the form
        #response = super().form_valid(form)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = 'active'
        context['title'] = 'Add a new Question for'
        context['topics'] = models.Topics.objects.get(id=self.kwargs['pk']).subject
        return context