from rest_framework import viewsets
from wagtail.core.models import Site
from wagtail_nav_menus.models import NavMenu
from wagtail_nav_menus.serializers import NavMenuSerializer


class NavMenuViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NavMenu.objects.all()
    serializer_class = NavMenuSerializer

    def get_queryset(self):
        site_id = self.request.GET.get('site', None)
        if site_id:
            try:
                self.request.site = Site.objects.get(id=site_id)
            except Site.DoesNotExist:
                pass
        qs = super().get_queryset()
        if self.request.site:
            qs = qs.filter(site=self.request.site)
        return qs
