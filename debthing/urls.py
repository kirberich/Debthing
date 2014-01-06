from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.main', name='main'),    
    url(r'^(?P<expense_pk>\d+)/?$', 'core.views.expense', name='expense'),
    url(r'^register/?$', 'core.views.register', name='register'),
    url(r'^overview/(?P<user_pk>\d*)/?$', 'core.views.overview', name='overview'),
    url(r'^login/?$', 'core.views.login_view'),
    url(r'^logout/?$', 'core.views.logout_view'),

    # Api
    url(r'^api/user/?$', 'core.views.api_user', name='api_user'),
    url(r'^api/add_friend/?$', 'core.views.api_add_friend', name='api_add_friend'),
    url(r'^api/expense/(?P<expense_pk>\d*)/?$', 'core.views.api_expense', name='api_expense'),
    url(r'^api/item/(?P<item_pk>\d*)/?$', 'core.views.api_item', name='api_item'),
)
