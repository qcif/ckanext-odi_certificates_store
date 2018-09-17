import json
from logging import getLogger

import ckan.lib.jobs as jobs
import ckan.plugins.toolkit as t
from ckan import model


class Certificates_Importer(object):
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.log = getLogger(__name__)

    def odi_certificate_level_import_all(self):
        response = t.get_action('odi_certificates_get_all')
        self.log.debug('import all response is %r' % response)
        for certificate in response.text.certificates:
            location = certificate.uri
            if not location:
                t.abort(404, "Unable to find certificate location")
            location_json = location + '.json'
            self.odi_certificate_level_import_job(location_json)
            self.log.info("Queued: %s" % location_json)

    def odi_certificate_level_import_jobs_list(self, data_ids):
        for data_id in data_ids:
            self.odi_certificate_level_import_job(data_id)

    def odi_certificate_level_import_job(self, id):
        try:
            jobs.enqueue(odi_certificate_level_import, [id])
            self.log.info("Odi certificate import queued: %s", id)
        except ValueError, e:
            self.log.error(e)

def odi_certificate_level_import(id):
    log = getLogger(__name__)
    context = ckan_context()
    response = t.get_action('odi_certificate_get_from_id')(context, {'id': id})
    log.debug('import response is %r', response)
    data_dict = response
    data_dict['id'] = id
    update_response = t.get_action('level_update')(context, data_dict=data_dict)
    log.debug('update response is %r' % update_response)


def ckan_context():
    return {
        'model': model,
        'session': model.Session,
        'user': t.c.user,
        'auth_user_obj': t.c.userobj,
    }
