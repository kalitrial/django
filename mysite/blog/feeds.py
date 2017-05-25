from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

"""subclass Feed of syndication framework. The title, link and description attributes correspond to the <title>, <link> and
 <description> RSS elements respectively
"""
class LatestPostsFeed(Feed):
    title = 'Knowledge today'
    link = '/blog/'
    description = 'Latest updates.'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)

