import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class Odi_Certificates_StorePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'odi_certificates_store')

    # IRoutes

    def before_map(self, map):
        odi_certificate_controller = 'ckanext.odi_certificates_store.controllers.odi_certificate:OdiCertificateController'
        map.connect('odi_certificate_level_update', '/odi_certificate_level_update',
                    controller=odi_certificate_controller,
                    action='odi_certificate_level_update')
        map.connect('odi_certificate_update', '/odi_certificate_update', controller=odi_certificate_controller,
                    action='odi_certificate_update')
        return map
