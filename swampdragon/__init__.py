def autodiscover_routes():
    """
    Auto-discover, borrowed from django admin
    """
    from django.conf import settings
    from django.utils.importlib import import_module
    imported_routers = []
    for app in settings.INSTALLED_APPS:
        try:
            target_mod = '%s.routers' % app
            if target_mod not in imported_routers:
                import_module(target_mod)
            imported_routers.append(target_mod)
        except ImportError:
            pass
