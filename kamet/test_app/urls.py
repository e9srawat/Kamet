from django.urls import path

from . import views

urlpatterns = [
    path("", views.AdminPanel.as_view(), name="index"),
    path("topics", views.Topics.as_view(), name="topics"),
    path("add_topic", views.AddTopic.as_view(), name="add_topic"),
    path("del_topic/<int:pk>/", views.DelTopic.as_view(), name="del_topic"),
    path("edit_topic/<int:pk>/", views.UpdateTopic.as_view(), name="edit_topic"),
    
    path("add_user", views.AddUser.as_view(), name="add_user"),
    path("edit_user/<int:pk>/", views.UpdateUser.as_view(), name="edit_user"),
    
    path("questions/<int:pk>/", views.TopicQuestions.as_view(), name="questions"),
    path("add_question/<int:pk>/", views.AddQuestion.as_view(), name="add_question"),

]