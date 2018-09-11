import ckan.plugins as p

from ckanext.odi_certificates_store.jobs import odi_certificate_level_import_jobs_list, odi_certificate_level_import_all


class OdiCertificatesCommand(p.toolkit.CkanCommand):
    summary = __doc__.split('\n')[0]
    usage = __doc__
    max_args = None
    min_args = 1

    def __init__(self, name):
        super(OdiCertificatesCommand, self).__init__(name)

    def command(self):
        import logging

        self._load_config()
        self.log = logging.getLogger("ckan.lib.cli")

        cmd = self.args[0]
        if cmd == 'fetch':
            if len(self.args) == 2:
                data_ids = [s.strip() for s in self.args[1].split(' ')]
                self.log.info("Running odi certificate import => %s", data_ids)
                odi_certificate_level_import_jobs_list(data_ids)
        elif cmd == 'fetchall':
            self.log.info("Running odi certificate import all")
            odi_certificate_level_import_all()
        else:
            self.parser.error('Command not recognized: %r' % cmd)
