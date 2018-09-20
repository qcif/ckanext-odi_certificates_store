from logging import getLogger

import ckan.lib.jobs as jobs
import ckan.plugins.toolkit as t
from ckan import model

log = getLogger(__name__)


class Certificates_Importer(object):
    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.log = getLogger("ckan.lib.cli")

    def odi_certificates_all_jobs(self, jobs_fn):
        try:
            jobs.enqueue(odi_certificates_all_process, [jobs_fn])
            self.log.info("Odi certificate all jobs queued: %s", str(jobs_fn))
        except ValueError, e:
            self.log.error(e)

    def odi_certificates_multiple_jobs(self, data_ids, job_fn):
        for data_id in data_ids:
            self.odi_certificate_job(data_id, job_fn)

    def odi_certificate_job(self, id, job_fn):
        try:
            jobs.enqueue(job_fn, [id])
            self.log.info("Odi certificate job queued: %s", id)
        except ValueError, e:
            self.log.error(e)


def odi_certificates_all_process(post_process_fn):
    log.debug("Gathering all certificates...")
    responses = t.get_action('odi_certificates_get_all')(ckan_context())
    if responses.status_code == 200:
        responses_json = responses.json()
        log.debug('Import all response: %r', responses)
        for response_json in responses_json.get('certificates', {}):
            try:
                _validate_location(response_json)
                post_process_fn(response_json)
            except t.ValidationError as e:
                log.error("Unable to proceed further with this record. Reason: %s", e)
    else:
        log.info("Import aborted for all certificates jobs. Reason: %r", responses)


def odi_certificate_level_import(id):
    try:
        response = t.get_action('odi_certificate_get_from_id')(ckan_context(), {'id': id})
        _process_odi_certificate_response(response, id, odi_certificate_level_update)
    except t.ValidationError as e:
        log.error("Unable to proceed further with this record. Reason: %s", e)


def _process_odi_certificate_response(response, id, post_process_fn):
    log.debug('import response is %r', response)
    if response.status_code == 200:
        response_json = response.json()
        certificate_json = t.get_or_bust(response_json, 'certificate')
        certificate_json['id'] = id
        log.debug('response post-process is now: %r', certificate_json)
        post_process_fn(certificate_json)
    else:
        log.info("Import aborted for %s. Reason: %r", id, response)


def odi_certificate_level_update(data_dict):
    log.debug("Sending data for level update: %r", data_dict)
    context = ckan_context()
    response = t.get_action('odi_certificate_level_as_extra_update')(context, data_dict=data_dict)
    log.info('Import response is %r' % response)
    return response


def _validate_location(response_json):
    # because an odi user can change the data title, \
    # we cannot rely on this from the response set. \
    # We need to go back and check for id against the documentation url
    log.info("Gathering data for %s", response_json['title'])
    location = _location(response_json)
    log.debug("Location found is: %s", location)
    documentation_url = _documentation_url(response_json)
    dataset_id = _guess_dataset_id(documentation_url)
    log.info("Trying %s as ckan dataset id...", dataset_id)
    _validate_dataset_id(dataset_id, location)
    response_json['id'] = dataset_id


def _guess_dataset_id(ckan_dataset_url):
    guessed_id = _url_last_path(ckan_dataset_url)
    return guessed_id


def _documentation_url(certificate):
    dataset = t.get_or_bust(certificate, 'dataset')
    return t.get_or_bust(dataset, 'documentationUrl')


def _url_last_path(url):
    return url.rsplit('/', 1)[-1]


def _validate_dataset_id(dataset_id, location):
    if not _is_dataset_id_valid_for_location(dataset_id, location):
        raise t.ValidationError("Dataset id: %s is not valid for location, %s", dataset_id, location)


def _is_dataset_id_valid_for_location(dataset_id, location):
    response = t.get_action('odi_certificate_get_from_id')(ckan_context(), {'id': dataset_id})
    if response.status_code == 200:
        response_json = response.json()
        certificate = response_json.get('certificate', {})
        location_from_id = _location(certificate)
        log.debug("Certificate location captured from dataset_id: %s, is: %s", dataset_id, location_from_id)
        return location == location_from_id
    else:
        raise t.ValidationError("Unable to validate dataset id: %s. Reason: %r", id, response)


def _location(certificate):
    log.debug('checking location(uri) in certificate: %r', certificate)
    location = t.get_or_bust(certificate, 'uri')
    return location + '.json'


def ckan_context():
    return {
        'model': model,
        'session': model.Session,
        'user': t.c.user,
        'auth_user_obj': t.c.userobj,
    }
