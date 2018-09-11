# import ckan.plugins.toolkit as t
#
# class OdiCertificatesJobs:
#
# def add_certficate_level_to_extras(context, id):
#     t.jobs.enqueue(,
#                  [self._get_task_context(context), self._get_package_data(data), True])
#
#
# def
#
#     def _update_certificate(context, package, certificate):
#         log.debug('update certificate called with context: %r', context)
#         log.debug('update certificate called with certificate: %r', certificate)
#         return requests.post(
#             urljoin(context['site_url'], '/api/3/action/certificate_assign'),
#             data=json.dumps({
#                 'id': package['id'],
#                 'certificate': certificate
#             }),
#             headers={
#                 'Authorization': context['apikey'],
#                 'content-type': 'application/json'
#             }
#         )