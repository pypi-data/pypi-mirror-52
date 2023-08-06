from django.db import models
from django.utils.translation import ugettext_lazy as _


class URLRewrite(models.Model):
    from_value = models.CharField(_("from value"), max_length=255, unique=True)
    to_value = models.CharField(_("to value"), max_length=255, unique=True)

    class Meta:
        verbose_name = _("URL rewrite")
        verbose_name_plural = _("URL rewrites")

    def __str__(self):
        return f"{self.from_value} -> {self.to_value}"
