from django.urls import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.conf import settings
from django.utils.translation import gettext as _

class RelatedFieldWidgetCanAdd(widgets.SelectMultiple):

    def __init__(self, related_model, related_url=None, person_id=None, *args, **kw):

        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

        if not related_url:
            rel_to = related_model
            info = (rel_to._meta.app_label, rel_to._meta.object_name.lower())
            related_url = 'admin:%s_%s_add' % info

        # Be careful that here "reverse" is not allowed
        self.related_url = related_url
        self.person_id = person_id

    def render(self, name, value, *args, **kwargs):
        self.related_url = reverse(self.related_url)#, args=[self.person_id])
        if self.person_id:
            self.related_url += f'?person_id={self.person_id}'
        output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
        output.append(u'<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
            (self.related_url, name))
        output.append(u'<img src="%sadmin/img/icon_addlink.gif" width="10" height="10" alt="%s"/></a>' % (settings.STATIC_URL, _('Add Another')))
        return mark_safe(u''.join(output))