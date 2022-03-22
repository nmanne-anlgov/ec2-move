import boto3
from dotenv import dotenv_values

CONFIG = dotenv_values()


def copy_sgroup():
    from_sess = boto3.Session(profile_name=CONFIG['FROM_PROFILE'])
    to_sess = boto3.Session(profile_name=CONFIG['TO_PROFILE'])

    from_ec2 = from_sess.resource('ec2')
    to_ec2 = to_sess.resource('ec2')

    vpcs = list(to_ec2.vpcs.all())
    assert len(vpcs) == 1
    vpc = vpcs[0]

    sgs = {}
    for sg in from_ec2.security_groups.all():
        sgs[sg.group_name] = sg

    for i, name in enumerate(sgs):
        print(f'{i}: {name}')
    si = input('Choose security group: ')

    sg = sgs[list(sgs.keys())[int(si)]]

    new_sg = to_ec2.create_security_group(
        Description=sg.description,
        GroupName=sg.group_name,
        VpcId=vpc.id,
    )

    new_sg.create_tags(Tags=sg.tags)
    new_sg.authorize_ingress(IpPermissions=sg.ip_permissions)
    # new_sg.authorize_egress(IpPermissions=sg.ip_permissions_egress)


if __name__ == '__main__':
    copy_sgroup()
