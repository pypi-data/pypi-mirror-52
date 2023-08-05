# k8s-leader-election-py
Client-go has a very easy to use leader-election package for kubernetes controllers to utilize [leader-election](https://github.com/kubernetes/client-go/blob/master/tools/leaderelection/leaderelection.go). The python kubernetes-client doesn't have such a method, so this will have to do for now.

## Requirements
Your controller must have a pod and namespace environment variable defined:
```yaml
env:
- name: POD
  valueFrom:
    fieldRef:
      fieldPath: metadata.name
- name: NAMESPACE
  valueFrom:
    fieldRef:
      fieldPath: metadata.namespace
```

Your controller must be able to list, get, update and create configmaps.
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: sample-controller
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: sample-controller
rules:
- apiGroups:
  - ""
  resources:
  - configmaps
  verbs:
  - '*'
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: sample-controller
roleRef:
  apiGroup: ""
  kind: Role
  name: sample-controller
subjects:
- kind: ServiceAccount
  name: sample-controller
  apiGroup: ""
```

## Example
Sample code:
```python
from threading import Thread
from leaderelection import Elect

# Init leader election class. Configmap is the name of the configmap to create to store leader election information
leaderelection = Elect(configmap='sample-controller-leader-election')
# Run leader election in new thread
th = Thread(target=leaderelection.run)
th.setDaemon(True)
th.start()
#start main controller loop
while True:
    # Check if pod is the leader. If so continue on with controller logic.
    leader = leaderelection.check_leader()
    if leader:
        logger.info("I am the leader!!")
    else:
        logger.info("I am NOT the leader")
```
