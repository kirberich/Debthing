from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    description = models.CharField(max_length=255)

    def __repr__(self):
        return self.description
    __unicode__ = __repr__

class Expense(BaseModel):
    def items_with_user(self, user):
        return Item.objects.filter(expense=self).filter(users=user)

class Item(BaseModel):
    class Meta:
        ordering = ['expense']
    expense = models.ForeignKey(Expense, related_name="items")
    amount = models.FloatField(default=0)
    users = models.ManyToManyField(User, related_name='assigned_items')

    def amount_per_user(self):
        return self.amount/self.users.all().count()

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    friends_pending = models.ManyToManyField('self', symmetrical=False)
    friends = models.ManyToManyField('self')

    def __repr__(self):
        return self.user.__repr__()
    __unicode__ = __repr__

    def self_and_friends(self):
        return set([self] + list(self.friends.all()))

    def items_with_user(self, other_user):
        return Item.objects.filter(created_by=self.user).filter(users=other_user)

    def reverse_items_with_user(self, other_user):
        return Item.objects.filter(created_by=other_user).filter(users=self.user)

    def balance_with_user(self, other_user, per_expense=False):
        # Balance is positive if user owes other_user, negative otherwise
        balance = {} if per_expense else 0

        items = self.items_with_user(other_user)
        for item in items:
            amount = item.amount_per_user()
            if per_expense:
                balance[item.expense] = balance.setdefault(item.expense, 0) - amount
            else:
                balance -= amount

        items = self.reverse_items_with_user(other_user)
        for item in items:
            amount = item.amount_per_user()
            if per_expense:
                balance[item.expense] = balance.setdefault(item.expense, 0) + amount
            else:
                balance += amount

        return balance

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])