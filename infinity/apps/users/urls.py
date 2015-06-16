from django.conf.urls import patterns, url
from users.views import login
from users.views import register
from users.views import UserDetailView
from users.views import UserUpdateView
from users.views import UserProfileView


urlpatterns = patterns(
    '',
    url("^login/$", login, name="login"),
    url("^register/$", register, name="register"),
    url(
        r'^update/$',
        UserUpdateView.as_view(),
        name="user-update"
    ),
    url(
        r'^(?P<slug>\w+)/$',
        UserDetailView.as_view(),
        name="user-detail"
    ),
)
