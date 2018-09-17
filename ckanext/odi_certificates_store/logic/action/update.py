from logging import getLogger

import ckan.plugins.toolkit as t

from ckanext.odi_certificates_store.lib.package_odi_certificate import merge_odi_certificate_with_package_extras, \
    validate, validate_odi_certificate_level, merge_package_extras

log = getLogger(__name__)


def odi_certificate_level_update(context=None, data_dict=None):
    odi_certificate = validate_odi_certificate_level(data_dict)
    cert_data = {
        'id': data_dict.get('id'),
        'odi_certificate': {
            'level': odi_certificate['level']
        }}
    return t.get_action('odi_certificate_update_extras')(context, dict(cert_data))


def odi_certificate_update_extras(context=None, data_dict=None):
    log.debug('incoming data dict for update extras is: %r', data_dict)
    log.debug('incoming context is: %r', context)
    validate(data_dict)
    id = data_dict['id']
    package_data_dict = t.get_action('package_show')(context, {'id': id})
    merge_odi_certificate_with_package_extras(package_data_dict, data_dict)
    return _update_package(context, package_data_dict)


def level_update(context=None, data_dict=None):
    odi_certificate = validate_odi_certificate_level(data_dict)
    id = data_dict['id']
    package_data_dict = t.get_action('package_show')(context, {'id': id})
    merge_package_extras(package_data_dict, {'level': odi_certificate['level']})
    return _update_package(context, package_data_dict)


def _update_package(context=None, data_dict=None):
    context['id'] = id
    context['api_version'] = 3,
    return t.get_action('package_update')(context, data_dict)
