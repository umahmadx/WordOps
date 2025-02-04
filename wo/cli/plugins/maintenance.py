"""Maintenance Plugin for WordOps"""

from cement.core.controller import CementBaseController, expose
from cement.core import handler, hook
from wo.core.logging import Log
from wo.core.variables import WOVariables
from wo.core.aptget import WOAptGet
from wo.core.apt_repo import WORepo
from wo.core.services import WOService
from wo.core.shellexec import WOShellExec



def wo_maintenance_hook(app):
    pass


class WOMaintenanceController(CementBaseController):
    class Meta:
        label = 'maintenance'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = ('update server packages to latest version')
        usage = "wo maintenance"

    @expose(hide=True)
    def default(self):

        try:
            Log.info(self, "updating apt-cache, please wait...")
            WOShellExec.cmd_exec(self, "apt-get update")
            Log.info(self, "updating packages, please wait...")
            WOShellExec.cmd_exec(self,  "DEBIAN_FRONTEND=noninteractive "
                                 "apt-get -o "
                                 "Dpkg::Options::='--force-confmiss' "
                                 "-o Dpkg::Options::='--force-confold' "
                                 "-y dist-upgrade")
            Log.info(self, "cleaning-up packages, please wait...")
            WOShellExec.cmd_exec(self, "apt-get -y --purge autoremove")
            WOShellExec.cmd_exec(self, "apt-get -y autoclean")
        except OSError as e:
            Log.debug(self, str(e))
            Log.error(self, "Package updates failed !")
        except Exception as e:
            Log.debug(self, str(e))
            Log.error(self, "Packages updates failed !")


def load(app):
    # register the plugin class.. this only happens if the plugin is enabled
    handler.register(WOMaintenanceController)
    # register a hook (function) to run after arguments are parsed.
    hook.register('post_argument_parsing', wo_maintenance_hook)
