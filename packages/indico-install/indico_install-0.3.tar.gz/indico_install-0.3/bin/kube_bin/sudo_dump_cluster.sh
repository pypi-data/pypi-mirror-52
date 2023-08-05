#! /bin/bash
set -e
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
outfile="cluster-info-${timestamp}.tar.gz"
dumpdir="./cluster_${timestamp}"

echo "Fetching cluster information..."
kubectl cluster-info dump -o yaml --output-directory=${dumpdir}
kubectl get secrets --namespace=default -o yaml > ${dumpdir}/secrets.yaml
kubectl get configmaps --namespace=default -o yaml > ${dumpdir}/configmaps.yaml
kubectl get ingress --namespace=default -o yaml > ${dumpdir}/ingress.yaml
kubectl get pv --namespace=default -o yaml > ${dumpdir}/pv.yaml
kubectl get pvc --namespace=default -o yaml > ${dumpdir}/pvc.yaml
echo "Compressing contents..."
tar -czf ${outfile} ${dumpdir}
rm -r ${dumpdir}
echo "Saved ${outfile}. Please email this to your indico contact. Thank you!"
