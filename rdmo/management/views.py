import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View
from rdmo.core.imports import handle_uploaded_file
from rdmo.core.xml import flat_xml_to_elements, read_xml_file

from .imports import check_permissions, import_elements

logger = logging.getLogger(__name__)


class UploadView(LoginRequiredMixin, View):

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER') or reverse('home')

    def get(self, request):
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request):
        try:
            uploaded_file = request.FILES['uploaded_file']
        except KeyError:
            return HttpResponseRedirect(self.get_success_url())
        else:
            import_tmpfile_name = handle_uploaded_file(uploaded_file)

        root = read_xml_file(import_tmpfile_name)
        if root is None:
            logger.info('Xml parsing error. Import failed.')
            return render(request, 'core/error.html', {
                'title': _('Import error'),
                'errors': [_('The content of the xml file does not consist of well formed data or markup.')]
            }, status=400)

        else:
            elements = flat_xml_to_elements(root)
            if check_permissions(elements, request.user):
                # store information in session for ProjectCreateImportView
                request.session['import_tmpfile_name'] = import_tmpfile_name
                request.session['import_success_url'] = self.get_success_url()

                return render(request, 'management/upload.html', {
                    'file_name': uploaded_file.name,
                    'elements': import_elements(elements)
                })
            else:
                return render(request, 'core/error.html', {
                    'title': _('Import error'),
                    'errors': [_('Forbidden.')]
                }, status=403)


class ImportView(LoginRequiredMixin, View):

    def get_success_url(self):
        return self.request.session.get('import_success_url') or reverse('home')

    def get(self, request):
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request):
        import_tmpfile_name = request.session.get('import_tmpfile_name')
        checked = [key for key, value in request.POST.items() if 'on' in value]

        root = read_xml_file(import_tmpfile_name)
        if root is None:
            logger.info('Xml parsing error. Import failed.')
            return render(request, 'core/error.html', {
                'title': _('Import error'),
                'errors': [_('The content of the xml file does not consist of well formed data or markup.')]
            }, status=400)

        else:
            elements = flat_xml_to_elements(root)
            if check_permissions(elements, request.user):
                import_elements(elements, save=checked)
                return HttpResponseRedirect(self.get_success_url())
            else:
                return render(request, 'core/error.html', {
                    'title': _('Import error'),
                    'errors': [_('Forbidden.')]
                }, status=403)