from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
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
from rest_framework import generics
from . import serializers


# Create your views here.
class AdminHome(TemplateView):
    template_name = 'base.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bg"] = "background-image: url('/static/back.jpg');"
        return context
    

class UserSubmissions(ListView):
    template_name = "admin_base.html"
    model = models.TestUser
    context_object_name = 'olist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Users & Submissions'
        context['status_user'] = 'active'
        context['header'] = [('Users','pass'),('Questions Attempted', 'text-end'),('Score', 'text-end'),('Attempts left', 'text-end')]
        context['svg'] = [{'image':'svgs/sliders.svg','link':'edit_user', 'params':'', 'delete':''},{'image':'svgs/trash-fill.svg','link':'', 'params':'data-mdb-ripple-init data-mdb-modal-init', 'delete':'del_user'}]
        context['link'] = 'solutions'
        context['add'] = ('add_user', "Add User")
        return context
    
class Topics(ListView):
    template_name = "admin_base.html"
    model = models.Topics
    context_object_name = 'olist'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_topic'] = 'active'
        context['title'] = 'All Topics'
        context['header'] = [('Topic','pass'),('Number of questions', 'text-end')]
        context['svg'] =  [{'image':'svgs/sliders.svg','link':'edit_topic', 'params':'', 'delete':''},{'image':'svgs/trash-fill.svg','link':'', 'params':'data-mdb-ripple-init data-mdb-modal-init', 'delete':'del_topic'}]
        context['link'] = 'questions'
        context['td_classes'] = {'third':'d-none','fourth':'d-none'}
        context['add'] = ('add_topic',"Add Topic")
        return context

class AddTopic(CreateView):
    template_name = 'add.html'
    form_class = forms.TopicForm
    success_url = 'topics'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_topic'] = 'active'
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
        context['status_topic'] = 'active'
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
        context['status_user'] = 'active'
        context['title'] = 'Add a new User'
        return context
    
class UpdateUser(UpdateView):
    model = models.TestUser
    template_name = 'add.html'
    form_class = forms.UpdateUserForm
    success_url = reverse_lazy("index")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_user'] = 'active'
        context['title'] = 'Edit User'
        return context
    
class DeleteUser(DeleteView):
    model = models.TestUser
    template_name = None
    success_url = reverse_lazy("index")
    
    
class TopicQuestions(ListView):
    template_name = "list.html"
    model = models.Question
    context_object_name = 'olist'
    
    def get_queryset(self):
        return self.model.objects.filter(topics=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Questions for'
        context['self'] = models.Topics.objects.get(id=self.kwargs['pk'])
        context['svg'] = [{'image':'svgs/pencil-square.svg','link':"edit_ques", 'params':'', 'delete':''},{'image':'svgs/trash-fill.svg','link':'', 'params':'data-mdb-ripple-init data-mdb-modal-init', 'delete':'del_ques'}]
        context['add'] = ('add_question', 'Add Question')
        return context
    
class AddQuestion(CreateView):
    template_name = 'add.html'
    form_class = forms.QuestionForm
    
    def form_valid(self, form: BaseModelForm):
        form.instance.topics = models.Topics.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)
    
    def get_success_url(self):
        """returns success_url"""
        return reverse_lazy("questions", kwargs={"pk": self.object.topics.id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_topic'] = 'active'
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
        context['status_topic'] = 'active'
        context['title'] = 'Edit Question'
        return context
    
class UserSolutionsView(ListView):
    template_name = "admin_base.html"
    model = models.Topics
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tuser']= models.TestUser.objects.get(id=self.kwargs['pk'])
        context['status_user'] = 'active'
        context['title'] = 'Solutions for '+str(context['tuser'])
        context['header'] = [('Topic','pass'),('Questions Attempted', 'text-end'),('Score', 'text-end')]
        context['olist'] = [{'subject':i,'num_solutions':i.solutions(context['tuser']),'score':i.score(context['tuser']),'links':2} for i in context['object_list']]
        context['link'] = 'topic_solutions' 
        context['td_classes'] = {'fourth':'d-none'}
        return context
    
class TopicSolutions(ListView):
    template_name = 'list.html'
    model = models.UserSolution
    context_object_name = 'olist'
    
    def get_queryset(self):
        return self.model.objects.filter(test_user=self.kwargs['user'],question__topics = self.kwargs['topic'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_user'] = 'active'
        context['title'] = f'{models.TestUser.objects.get(id=self.kwargs["user"])}\'s Submitted Solutions for {models.Topics.objects.get(id=self.kwargs["topic"])}'
        return context
    
class UserDash(ListView):
    """
    User's Dashboard
    """
    template_name = 'card.html'
    model = models.Topics
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bg"] = "background-image: url('/static/output.png');"
        context["status_user"] = 'd-none'
        context["status_topic"] = 'd-none'
        return context
    
    
class Rules(TemplateView):
    template_name = 'rules.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["topic"] = models.Topics.objects.get(id=self.kwargs["pk"])
        context["tuser"] = models.TestUser.objects.all()[1]
        context["status_user"] = 'd-none'
        context["status_topic"] = 'd-none'
        return context
    
class Test(TemplateView):
    template_name = 'temp.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        t = models.Topics.objects.all()[2]
        tu = models.TestUser.objects.all()[1]
        context["olist"] = t.random_question(tu)
        context["title"] = "Start test"
        return context
    
    def post(self, request, *args, **kwargs):
            tu = models.TestUser.objects.all()[1]
            us = list(request.POST.items())[1:]
            for i in us:
                question = models.Question.objects.get(id=i[0])
                models.UserSolution(test_user=tu, question=question, solution=i[1]).save()
            return redirect('users')


### API ###
class TuserListView(generics.ListCreateAPIView):
    queryset = models.TestUser.objects.all()
    serializer_class = serializers.TestUserSerializer
    
class TuserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.TestUser.objects.all()
    serializer_class = serializers.TestUserSerializer
    
class TopicsListView(generics.ListCreateAPIView):
    queryset = models.Topics.objects.all()
    serializer_class = serializers.TopicSerializer
    
class TopicsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Topics.objects.all()
    serializer_class = serializers.TopicSerializer
    lookup_field = 'slug'

class QuestionsListView(generics.ListCreateAPIView):
    serializer_class = serializers.QuestionSerializer
    
    def get_queryset(self):
        topic = models.Topics.objects.get(slug=self.kwargs['slug'])
        return models.Question.objects.filter(topics=topic)
    
    def perform_create(self, serializer):
        topic = models.Topics.objects.get(slug=self.kwargs['slug'])
        serializer.validated_data['topics'] = topic
        serializer.save()
    
class QuestionsDetailView(generics.RetrieveUpdateDestroyAPIView):
    #queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    lookup_field = 'quesno'
    
    def get_queryset(self):
        topic = models.Topics.objects.get(slug=self.kwargs['slug'])
        return models.Question.objects.filter(topics=topic)
    