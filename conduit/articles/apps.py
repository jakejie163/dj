from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    name = 'articles'
    label = 'articles'
    verbose_name = 'Articles'

    def ready(self):
        import articles.signals
