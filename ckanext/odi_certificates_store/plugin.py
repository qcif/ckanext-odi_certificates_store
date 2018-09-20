import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.odi_certificates_store.logic.action.update as action_update


class Odi_Certificates_StorePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IActions, inherit=True)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'odi_certificates_store')

    # IActions
    def get_actions(self):
        return {'odi_certificate_as_extra_update': action_update.odi_certificate_as_extra_update,
                'odi_certificate_level_as_extra_update': action_update.odi_certificate_level_as_extra_update
                }
