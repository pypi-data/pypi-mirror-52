import logging

import requests

from .spot_instance_monitor import SpotInstanceMonitor


logger = logging.getLogger(__name__)


class AwsSpotInstanceMonitor(SpotInstanceMonitor):

    TERMINATION_URL = 'http://169.254.169.254/latest/meta-data/spot/termination-time'
    TERMINATION_MSG = 'Spot instance marked for termination'

    def check_termination_time(self):
        response = requests.get(self.TERMINATION_URL)
        if response.status_code == 404:
            logging.debug('Spot instance not marked for termination')
            return ''  # will be ignored

        logging.warning(self.TERMINATION_MSG)
        return 'WARNING: {}'.format(self.TERMINATION_MSG)
