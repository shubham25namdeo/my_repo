from django.conf.urls import url

urlpatterns = [
    url(r'^register/$', ('first_app.views.register_user')),
    url(r'^success/', ('first_app.views.register_success')),
    url(r'^confirm/(?P<activation_key>\w+)/', ('first_app.views.register_confirm')),
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    url(r'^logout/$', ('first_app.views.logout_page')),
    url(r'^chats/$', ('first_app.views.chats')),
    url(r'^docx/$', ('first_app.views.docs')),
    url(r'^articles/$', ('first_app.views.articles')),
    url(r'^home/$', ('first_app.views.home')),
    url(r'^notes/$', ('first_app.views.newnotes')),
]

# from django.conf.urls import url, include
# from django.contrib import admin
# from first_app.views import *
#
# urlpatterns = [
#     url(r'^$', 'django.contrib.auth.views.login'),
#     url(r'^logout/$', logout_page),
#     url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
#     url(r'^register/$', register),
#     url(r'^register/success/$', register_success),
#     url(r'^home/$', home),
# ]