from logging import getLogger

import ckan.plugins.toolkit as t

from ckanext.odi_certificates_store.lib.package_odi_certificate import merge_odi_certificate_dict_into_package_extras, \
    validate, merge_package_extras

log = getLogger(__name__)


def odi_certificate_as_extra_update(context=None, data_dict=None):
    validate(data_dict)
    id = data_dict.pop('id')
    package_data_dict = t.get_action('package_show')(context, {'id': id})
    merge_odi_certificate_dict_into_package_extras(package_data_dict, data_dict)
    return _update_package(context, package_data_dict)


def odi_certificate_level_as_extra_update(context=None, data_dict=None):
    validate(data_dict)
    package_data_dict = t.get_action('package_show')(context, {'id': data_dict['id']})
    merge_package_extras(package_data_dict, {'odi_certificate_level': data_dict['level']})
    return _update_package(context, package_data_dict)


def _update_package(context=None, data_dict=None):
    context['id'] = t.get_or_bust(data_dict, 'id')
    context['api_version'] = 3,
    return t.get_action('package_update')(context, data_dict)
