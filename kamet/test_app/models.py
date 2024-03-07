"""models.py"""

import random
from django.db import models
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password


# Create your models here.
class TestUser(models.Model):
    """TestUser model"""
    User=get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test_user")
    attempts = models.IntegerField(default=1)
    

    def delete(self, using=None, keep_parents=False):
        """Deletes the User and the testuser"""
        self.user.delete()
        return super().delete(using, keep_parents)

    def attempted(self):
        """Decrement the attempts counter by 1 whenever user attempts a test"""
        self.attempts -= 1
        self.save()

    def send_email(self, password):
        '''sends email to user with their credentials'''
        subject = "Welcome to Kamet"
        message = f'''You can login and give the test AT WWW.EXAMPLE.COM \n
        your username is "{self.user.username}" and your password is "{password}"'''
        from_email = "shivansh.rawat@enine.school"
        recipient = [self.user.email]
        send_mail(subject, message, from_email, recipient)
    
    def num_solutions(self):
        return self.user_solution.all()
        
    def random_data(self):
        ulst = []
        tlst = []
        password = make_password('Qwerty@123')
        for i in range(1,10001):
            username = 'username'+str(i)
            email = username+"@email.com"
            ulst.append(self.User(
                username=username, password=password, email=email
            ))
            print(i,' user added' )
        self.User.objects.bulk_create(ulst)

        for j in ulst:
            tlst.append(TestUser(user=j, attempts=5))
        TestUser.objects.bulk_create(tlst)
    def __str__(self):
        return str(self.user)


class Topics(models.Model):
    """Topics model"""

    subject = models.CharField(max_length=20)
    time_allotted = models.IntegerField(default=60)
    number_questions = models.IntegerField(default=10)

    def random_question(self, testuser):
        """get number_questions number of questions for the topics"""
        user_solved_questions = [i.question.id for i in testuser.user_solution.all()]
        available_questions = self.qtopics.exclude(id__in=user_solved_questions)
        random_questions = random.sample(
            list(available_questions),
            min(self.number_questions, len(available_questions)),
        )
        return random_questions
    
    def num_questions(self):
        return self.qtopics
        
    def __str__(self):
        return str(self.subject)


class Question(models.Model):
    """Question model"""

    topics = models.ForeignKey(Topics, on_delete=models.CASCADE, related_name="qtopics")
    question_text = models.TextField()
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    option_d = models.CharField(max_length=100)
    options = [
        ("a", "A"),
        ("b", "B"),
        ("c", "C"),
        ("d", "D"),
    ]
    option_correct = models.CharField(max_length=1, choices=options)

    
    def __str__(self):
        return str(self.question_text)


class UserSolution(models.Model):
    """UserSolution model"""
    test_user = models.ForeignKey(
        TestUser, on_delete=models.CASCADE, related_name="user_solution"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="uquestion"
    )
    CHECK_CHOICES = [
        ("a", "A"),
        ("b", "B"),
        ("c", "C"),
        ("d", "D"),
    ]
    solution = models.CharField(max_length=1, choices=CHECK_CHOICES)

    def __str__(self):
        return str(self.solution)
