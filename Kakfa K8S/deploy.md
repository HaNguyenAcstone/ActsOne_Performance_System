helm repo add confluentinc https://confluentinc.github.io/cp-helm-charts/
helm repo update

helm install my-kafka confluentinc/cp-helm-charts -f my-kafka-values.yaml
