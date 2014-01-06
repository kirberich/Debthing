import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from models import Expense, Item
from django.contrib.auth.models import User

@login_required
def main(request):
    subs = {
        'expenses': Expense.objects.all(),
        'items':Item.objects.all(),
        'user': request.user,
        'users': User.objects.all(),
    }
    return render_to_response('main.html', subs, context_instance=RequestContext(request))

def expense(request, expense_pk):
    subs = {
        'expenses': Expense.objects.all(),
        'items':Item.objects.all(),
        'user': request.user,
        'users': User.objects.all(),
        'expense': Expense.objects.get(pk=expense_pk)
    } 
    return render_to_response('expense.html', subs, context_instance=RequestContext(request))

def register(request):
    subs = {
        'user': request.user
    }
    return render_to_response('register.html', subs, context_instance=RequestContext(request))

def overview(request, user_pk=None):
    subs = {
        'user': request.user
    }
    if user_pk:
        subs['other_user'] = User.objects.get(pk=user_pk)
        subs['friends'] = [subs['other_user'].profile] 
    else:
        subs['friends'] = request.user.profile.friends.all()
    return render_to_response('overview.html', subs, context_instance=RequestContext(request))

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render_to_response('login.html', {'error': "Balls."}, context_instance = RequestContext(request))
    else:
        return render_to_response('login.html', {"user": request.user}, context_instance = RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@require_POST
def api_user(request):
    user = request.user
    if not user.is_authenticated():
        user = User()
        user.username = request.POST.get('username')
        user.email = request.POST.get('username')
        user.set_password(request.POST.get('password'))
        user.save()

        user = authenticate(username=user.username, password=request.POST.get('password'))
        login(request, user)
    return HttpResponseRedirect('/')

@login_required
@require_POST
def api_add_friend(request):
    user = request.user
    profile = user.profile
    new_friend = User.objects.get(username=request.POST['user'])
    new_friend_profile = new_friend.profile

    # If the users added each other, confirm the friendship
    if new_friend_profile in profile.friends_pending.all():
        new_friend_profile.friends_pending.remove(profile)
        profile.friends_pending.remove(new_friend_profile)
        profile.friends.add(new_friend_profile)
    else:
        new_friend_profile.friends_pending.add(profile)
    return HttpResponseRedirect('/')

@login_required
@require_POST
def api_expense(request, expense_pk=None):
    if expense_pk:
        expense = Expense.objects.get(pk=expense_pk)
        if not expense.created_by == request.user:
            return HttpResponse(status=403)
    else:
        expense = Expense()
        expense.created_by = request.user
    expense.description = request.POST.get('description')
    expense.save()

    if request.is_ajax():
        return HttpResponse(json.dumps({'expense_description':expense.description}))
    return HttpResponseRedirect("/%s" % expense.pk)

@login_required
@require_POST
def api_item(request, item_pk=None):
    if item_pk:
        item = Item.objects.get(pk=item_pk)
        if not item.created_by == request.user:
            return HttpResponse(status=403)
    else:
        item = Item()
        item.created_by = request.user
    expense = Expense.objects.get(pk=request.POST.get('expense'))
    if not expense.created_by == request.user:
        return HttpResponse(status=403)
    item.expense = expense

    item.description = request.POST.get('description')
    item.amount = request.POST.get('amount')
    item.save()

    user_pks = request.POST.getlist('users')
    item.users.clear()
    for pk in user_pks:
        user = User.objects.get(pk=pk)
        item.users.add(user)

    return HttpResponseRedirect("/%s" % item.expense_id)
