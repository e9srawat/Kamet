from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponseRedirect, HttpResponse
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
    context_object_name = 'olist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        context['title'] = 'Users & Submissions'
        context['table'] = 'table table-striped'
        context['header'] = [('Users','pass'),('Questions Attempted', 'text-end')]
        context['svg'] = [('svgs/sliders.svg','edit_user'),('svgs/trash-fill.svg','','data-mdb-ripple-init data-mdb-modal-init')]
        context['delete'] = 'del_user'
        context['link'] = 'solutions'
        context['addr'] = ('add_user', "Add User")
        return context
    
class Topics(ListView):
    template_name = "admin_base.html"
    model = models.Topics
    context_object_name = 'olist'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = 'active'
        context['title'] = 'All Topics'
        context['table'] = 'table table-striped table-bordered'
        context['header'] = [('Topic','pass'),('Number of questions', 'text-end')]
        context['svg'] = [('svgs/pencil-square.svg',"edit_topic",''),('svgs/trash-fill.svg','','data-mdb-ripple-init data-mdb-modal-init')]
        context['delete'] = 'del_topic'
        context['link'] = 'questions'
        context['addr'] = ('add_topic',"Add Topic")
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
    
class DeleteUser(DeleteView):
    model = models.TestUser
    template_name = None
    success_url = reverse_lazy("index")
    
    
class TopicQuestions(ListView):
    template_name = "list.html"
    model = models.Question
    
    def get_queryset(self):
        return self.model.objects.filter(topics=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Questions for'
        context['self'] = models.Topics.objects.get(id=self.kwargs['pk'])
        context['svg'] = [('svgs/pencil-square.svg',"edit_ques",''),('svgs/trash-fill.svg','','data-mdb-ripple-init data-mdb-modal-init')]
        context['addr'] = ('add_question', 'Add Question')
        context['delete'] = 'del_ques'
        return context
    
class AddQuestion(CreateView):
    template_name = 'add.html'
    form_class = forms.QuestionForm
    
    def form_valid(self, form: BaseModelForm):
        print(self.kwargs['pk'])
        form.instance.topics = models.Topics.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)
    
    def get_success_url(self):
        """returns success_url"""
        return reverse_lazy("questions", kwargs={"pk": self.object.topics.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = 'active'
        context['title'] = 'Add a new Question for'
        context['topics'] = models.Topics.objects.get(id=self.kwargs['pk']).subject
        return context
    
class DelQuestion(DeleteView):
    model = models.Question
    template_name = None
    
    def get_success_url(self):
        """returns success_url"""
        return reverse_lazy("questions", kwargs={"pk": self.object.topics.id})
    
class UpdateQuestion(UpdateView):
    model = models.Question
    template_name = 'add.html'
    form_class = forms.QuestionForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = 'active'
        context['title'] = 'Edit Question'
        return context
    
class UserSolutionsView(ListView):
    template_name = "admin_base.html"
    model = models.Topics
    context_object_name = 'olist'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tuser']= models.TestUser.objects.get(id=self.kwargs['pk'])
        context['title'] = 'Solutions for '+str(context['tuser'])
        context['table'] = 'table table-striped table-bordered'
        context['header'] = [('Topic','pass'),('Questions Attempted', 'text-end')]
        context['olist'] = [(i,len(i.solutions(context['tuser']))) for i in context['object_list']]
        context['link'] = 'topic_solutions' 
        return context
    
class TopicSolutions(ListView):
    template_name = 'list.html'
    model = models.UserSolution
    
    def get_queryset(self):
        return self.model.objects.filter(test_user=self.kwargs['user'],question__topics = self.kwargs['topic'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Solutions submitted by {models.TestUser.objects.get(id=self.kwargs["user"])} for {models.Topics.objects.get(id=self.kwargs["topic"])}'
        print(context)
        return context
    
class UserDash(TemplateView):
    """
    User's Dashboard
    """
    template_name = 'card.html'