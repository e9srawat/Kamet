from rest_framework import serializers
from .models import TestUser, Question, Topics, UserSolution

class TestUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestUser
        fields = "__all__"
        

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = "__all__"
        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_text','option_a','option_b','option_c','option_d','option_correct']
        