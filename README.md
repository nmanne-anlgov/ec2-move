# ec2-move

Scripts to help move AWS resources from one account to another

## Use AWS config files to create profiles

### Examples:

### \<Home\>/.aws/credentials
```
[farshore]
aws_access_key_id = XX
aws_secret_access_key = XXXX

[govcloud]
aws_access_key_id = XX
aws_secret_access_key = XXXX
```

### \<Home\>/.aws/config
```
[profile farshore]
region = us-east-2

[profile govcloud]
region = us-gov-west-1
```
