# ecssh

fill out `~/.config/ecssh.yml`

```yaml
test:
  some_cluster_name:
    ssh_user: ec2-user
prod: # AWS ENVIRONMENT
  public_prod: # ECS CLUSTER NAME
    ssh_user: ec2-user
    ssh_key: ~/.ssh/aws.pem
  internal_one:
    ssh_user: ec2-user
    ssh_key: ~/.ssh/id_ed25519
```
