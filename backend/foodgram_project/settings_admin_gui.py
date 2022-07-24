"""
Jazzmin

Welcome to Jazzmin, intended as a drop-in app to jazz up your django admin
site, with plenty of things you can easily customise, including a built-in
UI customizer.

To configure the general behaviour of jazzmin, you can use JAZZMIN_SETTINGS
within your django settings, below is a full example, with some of the more
complex items explained below that.
https://django-jazzmin.readthedocs.io/configuration/
"""

JAZZMIN_SETTINGS = {
    'welcome_sign': 'Welcome Home, ashen one.',
    'copyright': 'VaeSemper',
}

JAZZMIN_UI_TWEAKS = {
    'navbar_small_text': False,
    'footer_small_text': True,
    'body_small_text': False,
    'brand_small_text': True,
    'brand_colour': 'navbar-secondary',
    'accent': 'accent-primary',
    'navbar': 'navbar-dark',
    'no_navbar_border': False,
    'navbar_fixed': True,
    'layout_boxed': False,
    'footer_fixed': False,
    'sidebar_fixed': True,
    'sidebar': 'sidebar-dark-primary',
    'sidebar_nav_small_text': True,
    'sidebar_disable_expand': False,
    'sidebar_nav_child_indent': False,
    'sidebar_nav_compact_style': False,
    'sidebar_nav_legacy_style': False,
    'sidebar_nav_flat_style': True,
    'theme': 'darkly',
    'dark_mode_theme': None,
    'button_classes': {
        'primary': 'btn-primary',
        'secondary': 'btn-secondary',
        'info': 'btn-outline-info',
        'warning': 'btn-outline-warning',
        'danger': 'btn-outline-danger',
        'success': 'btn-outline-success'
    },
    'actions_sticky_top': False
}
