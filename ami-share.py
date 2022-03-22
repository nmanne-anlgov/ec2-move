from datetime import datetime

import boto3
from dotenv import dotenv_values

CONFIG = dotenv_values()

TIMESTAMP = datetime.now().timestamp()


def main():
    from_sess = boto3.Session(profile_name=CONFIG['FROM_PROFILE'])
    to_sess = boto3.Session(profile_name=CONFIG['TO_PROFILE'])

    from_ec2 = from_sess.resource('ec2')

    to_ec2 = to_sess.client('ec2')
    to_sess_account = to_sess.client('sts').get_caller_identity()['Account']

    from_instance = from_ec2.Instance(CONFIG['INSTANCE_TO_COPY'])

    from_ami = from_instance.create_image(Name=f'MOVE-EC2_{TIMESTAMP}_{from_instance.id}')
    from_ami.wait_until_exists(Filters=[{'Name': 'state', 'Values': ['available']}])

    from_ami.modify_attribute(LaunchPermission={'Add': [{'UserId': to_sess_account}]})

    to_ec2.copy_image(Name=from_ami.name, SourceImageId=from_ami.id, SourceRegion=from_sess.region_name)
    input('Finished Sharing')
    from_ami.deregister()


if __name__ == '__main__':
    main()
