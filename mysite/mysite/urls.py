"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #telling Django to include the URL patterns defined in the blog urls.py under the blog path
    #You are giving the a namespace called blog so you can refer to this group of urls easily
    url(r'^blog/', include(
        'blog.urls',
        namespace='blog',
        app_name='blog'
    )),
    # include the required imports and define a dictionary of sitemaps. We define a URL pattern that matches with sitemap.xml
    # and uses the sitemap view. The sitemaps dictionary is passed to the sitemap view
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

]
