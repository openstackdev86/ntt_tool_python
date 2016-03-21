from novaclientutils import NovaClientUtils
from glanceclientutils import GlanceClientUtils


class VMManager(NovaClientUtils, GlanceClientUtils):

    def check_status(self):
        pass

    def destroy(self, vm_id=None):
        pass
