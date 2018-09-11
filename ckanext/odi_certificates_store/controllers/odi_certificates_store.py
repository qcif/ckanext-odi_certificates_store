from logging import getLogger

log = getLogger(__name__)

import ckan.plugins.toolkit as t


class OdiCertificatesStoreController(t.BaseController):

    # TODO: test validation error
    # TODO: test unauthorised error
    def odi_certificate_level_update(self):
        context = {
            'model': t.model,
            'session': t.model.Session,
            'user': t.c.user,
            'auth_user_obj': t.c.userobj,
            'odi_certificate': {'level': 'level' in t.request.params}
        }
        log.debug('context is %r' % context)
        odi_certificate = t.request.body.get('odi_certificate', {})
        if not odi_certificate.get('level', ''):
            t.abort(400,
                    'Data attribute, "odi_certificate", and "odi_certificate" attribute, "level", must both be present.')
        else:
            return self.odi_certificate_update()

    def odi_certificate_update(self):
        data_dict = t.request.body
        if not data_dict.get('odi_certificate', ''):
            t.abort(400, 'Data attribute, "odi_certificate", must be present.')
        if not data_dict.get('id', ''):
            t.abort(400, 'Data attribute, "id", must be present.')
        data_dict['extras'] = {}
        data_dict['extras']['odi_certificate'] = data_dict.pop('odi_certificate')
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

        return t.get_action('package_update_rest')(t.c, data_dict)
