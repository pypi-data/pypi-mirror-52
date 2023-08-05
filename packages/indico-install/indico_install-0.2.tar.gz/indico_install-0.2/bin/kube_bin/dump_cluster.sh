#! /bin/bash
set -e
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
outfile="cluster-info-${timestamp}.tar.gz"
dumpdir="./cluster_${timestamp}"

echo "Fetching cluster information..."
sudo kubectl cluster-info dump -o yaml --output-directory=${dumpdir}
sudo kubectl get secrets --namespace=default -o yaml > ${dumpdir}/secrets.yaml
sudo kubectl get configmaps --namespace=default -o yaml > ${dumpdir}/configmaps.yaml
sudo kubectl get ingress --namespace=default -o yaml > ${dumpdir}/ingress.yaml
sudo kubectl get pv --namespace=default -o yaml > ${dumpdir}/pv.yaml
sudo kubectl get pvc --namespace=default -o yaml > ${dumpdir}/pvc.yaml
echo "Compressing contents..."
tar -czf ${outfile} ${dumpdir}
rm -r ${dumpdir}
echo "Saved ${outfile}. Please email this to your indico contact. Thank you!"
