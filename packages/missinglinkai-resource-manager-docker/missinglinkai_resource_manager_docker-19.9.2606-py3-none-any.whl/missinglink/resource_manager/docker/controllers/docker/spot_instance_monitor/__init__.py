from .aws_spot_instance_monitor import AwsSpotInstanceMonitor

AWS_CLOUD_TYPE = 'aws'


def get_spot_instance_monitor(cloud_type):
    monitors = {
        AWS_CLOUD_TYPE: AwsSpotInstanceMonitor,
    }

    return monitors.get(cloud_type)
