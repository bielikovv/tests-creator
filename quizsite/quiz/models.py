from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    name = models.CharField(max_length=255, verbose_name='Test name')
    description = models.CharField(max_length=2000, verbose_name='Test description', blank=True, null=True)
    max_result = models.IntegerField(verbose_name='Max result')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date', null=True)
    completed_by_user = models.ManyToManyField('Profile', verbose_name='Completed by', blank=True)
    is_published = models.BooleanField(default=False, verbose_name='Is published')

    def __str__(self):
        return self.name



class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Test')
    content = models.TextField(verbose_name='Content')
    value = models.FloatField(verbose_name='Value')
    answer = models.ManyToManyField('Answer', verbose_name='Answer', blank=True)



class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', null=True)
    content = models.TextField(verbose_name='Answer content')
    is_right = models.BooleanField(default=True, verbose_name='Is right')



class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', null=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Test')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Question', null=True)
    result = models.FloatField(verbose_name='Result', blank=True, null=True)
    answer = models.ManyToManyField('Answer', verbose_name='Answer', blank=True)



class Rank(models.Model):
    rank = models.CharField(max_length=255, verbose_name='Rank')
    value = models.IntegerField(verbose_name='Value')

    def __str__(self):
        return self.rank



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='User', null=True, blank=True)
    created_test = models.ManyToManyField(Test, verbose_name='Created test', blank=True)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, verbose_name='Rank', default=1)




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
