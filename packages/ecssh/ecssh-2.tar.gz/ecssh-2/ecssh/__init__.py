import json

def listContainerInstances(ECS, CLUSTER):
    retval = ECS.list_container_instances(cluster=CLUSTER, maxResults=100)
    return retval.get("containerInstanceArns")


def listInstanceIDs(ECS, ContainerInstances, CLUSTER):
    retval = ECS.describe_container_instances(
        cluster=CLUSTER, containerInstances=ContainerInstances)
    instances = retval.get("containerInstances")
    IDs = list()
    for instance in instances:
        IDs.append(instance.get("ec2InstanceId"))
    return IDs


def listInstanceIPs(EC2, IDs):
    retval = EC2.describe_instances(InstanceIds=IDs)
    IPs = list()
    for item in retval.get("Reservations"):
        IPs.append(item.get("Instances")[0].get("PrivateIpAddress"))
    return IPs

def listClusters(ECS):
    retval = ECS.list_clusters(maxResults=100)
    CLUSTERS = list()
    for cluster in retval.get("clusterArns"):
        CLUSTERS.append(cluster.split("/")[-1])
    print(json.dumps(CLUSTERS))


def ecssh(CONFIG, ECS, EC2, CLUSTER=None, N=None):
    containerInstances = listContainerInstances(ECS, CLUSTER=CLUSTER)
    IDs = listInstanceIDs(ECS, containerInstances, CLUSTER)
    IPs = listInstanceIPs(EC2=EC2, IDs=IDs)

    if N:
        return "ssh {KEY} {USER}@{IP}".format(KEY=CONFIG.get(
            "ssh_key") or "", USER=CONFIG.get("ssh_user"), IP=IPs[N-1])
    else:
        for IP in IPs:
            print("ssh {KEY} {USER}@{IP}".format(KEY=CONFIG.get(
                "ssh_key") or "", USER=CONFIG.get("ssh_user"), IP=IP))
