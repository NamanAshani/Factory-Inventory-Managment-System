from django.apps import AppConfig


class StockConfig(AppConfig):

    # default primary key type
    default_auto_field = 'django.db.models.BigAutoField'

    # name of app
    name = 'stock'

    # this runs when Django starts
    def ready(self):

        # import signals so Django activates them
        import stock.signals
