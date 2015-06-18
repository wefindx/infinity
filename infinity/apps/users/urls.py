from django.conf.urls import patterns, url
from users.views import UserDetailView
from users.views import UserUpdateView
from users.views import UserCryptsyNotificationToken


urlpatterns = patterns(
    '',
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
    url(
        r'^(?P<username>\w+)/cryptsy/(?P<credential_id>\d+)/checkpoint/$',
        UserCryptsyNotificationToken.as_view(),
        name='cryptsy_notification_token'
    )
)
