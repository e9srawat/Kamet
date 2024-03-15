from django.urls import path

from . import views

urlpatterns = [
    path("", views.AdminHome.as_view(), name="index"),
    path("users", views.UserSubmissions.as_view(), name="users"),
    path("topics", views.Topics.as_view(), name="topics"),
    path("add_topic", views.AddTopic.as_view(), name="add_topic"),
    path("del_topic/<int:pk>/", views.DelTopic.as_view(), name="del_topic"),
    path("edit_topic/<int:pk>/", views.UpdateTopic.as_view(), name="edit_topic"),
    
    path("add_user", views.AddUser.as_view(), name="add_user"),
    path("edit_user/<int:pk>/", views.UpdateUser.as_view(), name="edit_user"),
    path("del_user/<int:pk>/", views.DeleteUser.as_view(), name="del_user"),
    
    path("questions/<int:pk>/", views.TopicQuestions.as_view(), name="questions"),
    path("add_question/<int:pk>/", views.AddQuestion.as_view(), name="add_question"),
    path("del_ques/<int:pk>/", views.DelQuestion.as_view(), name="del_ques"),
    path("edit_ques/<int:pk>/", views.UpdateQuestion.as_view(), name="edit_ques"),

    path("solutions/<int:pk>/", views.UserSolutionsView.as_view(), name="solutions"),
    path("topic_solutions/<int:user>/<int:topic>/", views.TopicSolutions.as_view(), name="topic_solutions"),

    path("dashboard", views.UserDash.as_view(), name="dashboard"),
    path("rules/<int:pk>/", views.Rules.as_view(), name="rules"),
    path("test", views.Test.as_view(), name="test"),
    
    
    path("api/users", views.TuserListView.as_view()),
    path("api/users/<int:pk>", views.TuserDetailView.as_view()),
    path("api/topics", views.TopicsListView.as_view()),
    path("api/topics/<slug:slug>", views.TopicsDetailView.as_view()),
    path("api/<slug:slug>/questions", views.QuestionsListView.as_view()),
    path("api/<slug:slug>/questions/<int:quesno>", views.QuestionsDetailView.as_view()),

]