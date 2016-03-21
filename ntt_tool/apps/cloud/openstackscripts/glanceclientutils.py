from glanceclient.v2 import client as glance_client
from openstackclientutils import OpenStackClientUtils
from config import *


class GlanceClientUtils(OpenStackClientUtils):
    client_class = glance_client.Client

    def __init__(self, **credentials):
        super(GlanceClientUtils, self).__init__(**credentials)
        self.glance = self.get_client_instance()

    def upload_image(self):
        image = self.glance.images.create(
                disk_format=GLANCE_IMAGE_DISK_FORMAT,
                container_format=GLANCE_IMAGE_CONTAINER_FORMAT,
                name=GLANCE_IMAGE_NAME)
        self.glance.images.upload(image.id, open(GLANCE_IMAGE_PATH, 'rb'))
        return image
