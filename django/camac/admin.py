from django.contrib.admin import AdminSite
from django.utils.translation import gettext as _


class DjangoAdminSite(AdminSite):
    login_template = "login.html"
    site_header = _("eBau")
    site_title = _("eBau")
    index_title = _("Administration")
