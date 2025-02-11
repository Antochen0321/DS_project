# To deploy nodes
kubectl apply -f kubernetes/deployment/node1-deployment.yaml
kubectl apply -f kubernetes/deployment/node2-deployment.yaml

# Pour exposed services
kubectl apply -f kubernetes/service/node1-service.yaml
kubectl apply -f kubernetes/service/node2-service.yaml

# To create persistant storages
kubectl apply -f kubernetes/storage/persistent-volume.yaml
kubectl apply -f kubernetes/storage/persistent-volume-claim.yaml
