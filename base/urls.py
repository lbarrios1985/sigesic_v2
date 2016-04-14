from django.conf.urls import url, patterns

urlpatterns = patterns(
    url(r'^inicio/$', 'base.views.inicio', name='inicio'),
)