import json
from logging import getLogger

from ckan import model

log = getLogger(__name__)

import ckan.plugins.toolkit as t


class OdiCertificatesStoreController(t.BaseController):

    # TODO: test validation error
    # TODO: test unauthorised error
    def odi_certificate_level_update(self):
        log.debug('context is %r', self.ckan_context())
        log.debug('request headers is %r', t.request.headers)
        log.debug('request body is %r', t.request.body)
        data = json.loads(t.request.body)
        odi_certificate = data.get('odi_certificate', {})
        if not odi_certificate.get('level', ''):
            t.abort(400, t._(
                'Data attribute, "odi_certificate", and "odi_certificate" attribute, "level", must both be present.'))
        cert_data = {
            'id': data['id'],
            'odi_certificate': {
                'level': odi_certificate['level']
            }}
        return self._odi_certificate_update_extras(dict(cert_data))

    def _odi_certificate_update_extras(self, data_dict):
        # if not data_dict.get('odi_certificate', ''):
        #     t.abort(400, 'Data attribute, "odi_certificate", must be present.')
        # if not data_dict.get('id', ''):
        #     t.abort(400, 'Data attribute, "id", must be present.')
        package_data_dict = t.get_action('package_show')(self.ckan_context(), {'id': data_dict.get('id')})
        # try:
        #     # pkg_dict = t.get_action('package_show')(context, {'id': data.get('id', '')})
        #     id = t.get_or_bust(data, 'id')
        # except t.NotAuthorized as e:
        #     t.abort(401, e)
        # except t.ValidationError as e:
        #     t.abort(409, e)

        # model = t.c['model']
        # package = model.Package.get(id)
        # if not package:
        #     t.abort(404, 'No existing package matched the given ID.')
        # return t.get_action('odi_certificate_update')(t.c, data)
        # data_dict['extras'] = {}
        package_extras = self.dictize_extras(package_data_dict)
        log.debug('extras are %r', package_extras)
        package_extras['odi_certificate'] = package_extras.get('odi_certificate', {})
        package_extras_odi_certificate = package_extras['odi_certificate']
        package_extras_odi_certificate.update(data_dict.get('odi_certificate', {}))
        extras_undict = self.undictize_extras(package_extras)
        package_data_dict['extras'] = extras_undict
        log.debug('package now is %r', package_data_dict)
        context = self.ckan_context()
        context['id'] = data_dict.get('id')
        context['api_version'] = 3,
        return t.get_action('package_update')(context, package_data_dict)

    def ckan_context(self):
        return {
            'model': model,
            'session': model.Session,
            'user': t.c.user,
            'auth_user_obj': t.c.userobj,
        }

    def dictize_extras(self, data_dict):
        extras = [[extra['key'], extra['value']] for extra
                  in data_dict.get('extras', [])]
        for extra in extras:
            try:
                extra[1] = json.loads(extra[1])
            except (ValueError, TypeError):
                pass
        extras_dict = dict(extras)
        log.debug('dictized extras: %r', extras_dict)
        return extras_dict

    def undictize_extras(self, extras_dict):
        extras_undict = [{'key': k, 'value': v}
                         for k, v in extras_dict.items()]
        for extra in extras_undict:
            value = extra['value']
            if isinstance(value, dict) or isinstance(value, list):
                extra['value'] = json.dumps(value)
        log.debug('undictized extras: %r', extras_undict)
        return extras_undict
