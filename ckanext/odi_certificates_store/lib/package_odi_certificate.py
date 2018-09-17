import json
from logging import getLogger

import ckan.plugins.toolkit as t

log = getLogger(__name__)


def merge_odi_certificate_with_package_extras(data_dict, odi_certificate_data_dict):
    extras = dictize_extras(data_dict)
    extras['odi_certificate'] = extras.get('odi_certificate', {})
    extras['odi_certificate'].update(odi_certificate_data_dict.get('odi_certificate', {}))
    extras_undict = undictize_extras(extras)
    data_dict['extras'] = extras_undict
    return data_dict

def merge_package_extras(data_dict, incoming_extras):
    extras = dictize_extras(data_dict)
    extras.update(incoming_extras)
    extras_undict = undictize_extras(extras)
    data_dict['extras'] = extras_undict
    return data_dict


def odi_certificate_from_data(data_dict):
    extras = dictize_extras(data_dict)
    odi_certificate = extras.get('odi_certificate', {})
    return odi_certificate


def dictize_extras(data_dict):
    extras = [[extra['key'], extra['value']] for extra in data_dict.get('extras', [])]
    for extra in extras:
        try:
            extra[1] = json.loads(extra[1])
        except (ValueError, TypeError):
            pass
    extras_dict = dict(extras)
    log.debug('dictized extras: %r', extras_dict)
    return extras_dict


def undictize_extras(extras_dict):
    extras_undict = [{'key': k, 'value': v}
                     for k, v in extras_dict.items()]
    for extra in extras_undict:
        value = extra['value']
        if isinstance(value, dict) or isinstance(value, list):
            extra['value'] = json.dumps(value)
    log.debug('undictized extras: %r', extras_undict)
    return extras_undict


def validate(data_dict):
    validate_odi_certificate(data_dict)
    validate_id(data_dict)


def validate_odi_certificate(data_dict):
    if not data_dict.get('odi_certificate', '') and data_dict.get('certificate', ''):
        data_dict['odi_certificate'] = data_dict.pop('certificate')
    if not data_dict.get('odi_certificate', ''):
        t.abort(400, t._('Data attribute, "odi_certificate", must be present.'))


def validate_odi_certificate_level(data_dict):
    log.debug('incoming data dict for level validation: %r', data_dict)
    odi_certificate = data_dict.get('certificate', {})
    if not odi_certificate.get('level', ''):
        t.abort(400, t._(
            'Data attribute, "certificate", and "certificate" attribute, "level", must both be present.'))
    return odi_certificate


def validate_id(data_dict):
    if not data_dict.get('id', ''):
        t.abort(400, t._('Data attribute, "id", must be present.'))
