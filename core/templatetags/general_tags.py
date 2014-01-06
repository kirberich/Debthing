from django import template
import locale

register = template.Library()

@register.filter(name='balance')
def balance(user, other_user):
	return user.profile.balance_with_user(other_user)

@register.filter(name='balance_per_expense')
def balance_per_expense(user, other_user):
	return user.profile.balance_with_user(other_user, per_expense=True)

@register.filter(name='items')
def items(user, other_user):
	return user.profile.items_with_user(other_user)

@register.filter(name='expense_items')
def expense_items(expense, user):
	return expense.items_with_user(user)

@register.filter(name='currency')
def currency(number):
	locale.setlocale( locale.LC_ALL, 'en_GB' )
	return locale.currency(number)

@register.filter(name='is_positive')
def is_positive(number):
	return number > 0