from logging import getLogger

import ckan.plugins.toolkit as t

log = getLogger(__name__)


def odi_certificate_level_import_all():
    response = t.get_action('odi_certificates_get_all')
    log.debug('import all response is %r' % response)
    for certificate in response.text.certificates:
        location = certificate.uri
        if not location:
            t.abort(404, "Unable to find certificate location")
        location_json = location + '.json'
        odi_certificate_level_import_job(location_json)
        log.info("Queued: %s" % location_json)


def odi_certificate_level_import_jobs_list(data_ids):
    for data_id in data_ids:
        odi_certificate_level_import_job(data_id)
    log.info("Odi certificate imports queued.")


def odi_certificate_level_import_job(id):
    log.debug('setting up odi certificates job...')
    try:
        t.enqueue_job(odi_certificate_level_import, [id], {}, id, 'odi_certificates')
    except ValueError, e:
        log.error(e)


# TODO: test validation error
# TODO: test unauthorised error
def odi_certificate_level_import(self, id):
    response = t.get_action('odi_certificate_get')(id)
    log.debug('import response is %r' % response)
    update_response = t.action('odi_certificate_level_update', ({}, response.text))
    log.debug('update response is %r' % update_response)
