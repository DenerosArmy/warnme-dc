"""Models for WarnMe DC"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class FoodTag(models.Model):
    """Food tag

    :ivar CharField name: Name of the tag
    :ivar ManyToManyField foods: All foods with this tag
    """
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Food(models.Model):
    """Food

    :ivar CharField name: Name of the food
    :ivar FloatField rating: Current rating of the food
    :ivar ManyToManyField tags: All tags for this food
    :ivar ManyToManyField user_ratings: User ratings for this food
    :ivar ManyToManyField offerings: All offerings of this food
    """
    name = models.CharField(max_length=60)
    rating = models.FloatField()
    tags = models.ManyToManyField(FoodTag, related_name='foods', blank=True)

    def __str__(self):
        return self.name

class UserRating(models.Model):
    """One user rating

    :ivar User user: User who made the rating
    :ivar DateTimeField time: Time the rating was added (automatically set to current time when the object is created)
    :ivar ManyToManyField food: Food that was rated
    :ivar FloadField rating: Rating for the food
    """
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    food = models.ForeignKey(Food, related_name='user_ratings')
    rating = models.FloatField()

    def __str__(self):
        return "USER {} AT {} RATES {} AS {}".format(
            self.user, self.time, self.food, self.rating)

class Offering(models.Model):
    """Food offerings for a given day

    :ivar Offering.LOCATION_CHOICES location: "Foothill", "Crossroads", "Cafe 3", or "Clark Kerr"
    :ivar DateField day: Day the food is offered. Must be set manually to a Python datetime.date instance
    :ivar Offering.MEAL_CHOICES meal: "Breakfast", "Lunch", "Dinner", or "Brunch"
    :ivar ManyToManyField foods: Foods being served
    """
    LOCATION_CHOICES = (
        ('FH', 'Foothill'),
        ('CR', 'Crossroads'),
        ('C3', 'Cafe 3'),
        ('CKC', 'Clark Kerr')
    )
    location = models.CharField(max_length=3, choices=LOCATION_CHOICES)

    date = models.DateField()

    MEAL_CHOICES = (
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner'),
        ('R', 'Brunch')
    )
    meal = models.CharField(max_length=1, choices=MEAL_CHOICES)

    foods = models.ManyToManyField(Food, related_name='offerings', blank=True)

    def __str__(self):
        return "{}: {} MEAL ON {}".format(
            self.location, self.meal, self.date)

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    default_location = models.CharField(max_length=3,
                                        choices=Offering.LOCATION_CHOICES,
                                        default='FH')
    blacklisted_tags = models.ManyToManyField(FoodTag,
                                              related_name='blacklist_users',
                                              blank = True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
