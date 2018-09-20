import ckan.plugins as p

from ckanext.odi_certificates_store.jobs import odi_certificate_level_import, odi_certificate_level_update


class OdiCertificatesCommand(p.toolkit.CkanCommand):
    """
    Import 1 or more odi certificate(s).

    The available commands are:

        import       - Import one or more odi certificates given a space-separated list of dataset IDs

        importall    - Import all odi certificates

    e.g.

        Import a single odi certificate (dataset ID = 'test2')
        $ paster import test2

        Import multiple odi certificates
        $ paster import test2 test3

        Import all odi certificates
        $ paster importall

    """

    summary = __doc__.split('\n')[1]
    usage = __doc__
    short_description = summary

    max_args = None
    min_args = 1

    def __init__(self, name):
        super(OdiCertificatesCommand, self).__init__(name)

    def command(self):
        import logging
        from ckanext.odi_certificates_store.jobs import Certificates_Importer

        self._load_config()
        self.log = logging.getLogger("ckan.lib.cli")

        cmd = self.args[0]
        try:
            importer = Certificates_Importer.instance()
            if cmd == 'import':
                if len(self.args) == 2:
                    data_ids = [s.strip() for s in self.args[1].split(' ')]
                    self.log.info("Running odi certificate import => %s", data_ids)
                    importer.odi_certificates_multiple_jobs(data_ids, odi_certificate_level_import)
                else:
                    self.parser.error('"import" needs at at least dataset ID')
            elif cmd == 'importall':
                self.log.info("Running odi certificate import all")
                importer.odi_certificates_all_jobs(odi_certificate_level_update)
            else:
                self.parser.error('Command not recognized: %r' % cmd)
        except ValueError, e:
            self.log.error(e)
        self.log.info("Command runner completed.")
