from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^in.php$', 'gw.views.input_captcha', name='input'),
    url(r'^res.php', 'gw.views.result_captcha', name='result'),
)
