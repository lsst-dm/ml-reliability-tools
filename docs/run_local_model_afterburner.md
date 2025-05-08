# Run a local model as an afterburner

## create local model 

* clone `meas_transinet`
* create a new directory in `model_packages`
* create `arch.py`, `checkpoint.pt`, `meta.yaml`

## DRP

`setup -kr meas_transinet`

use something like `pipelines/DRPRBAfterburner.yaml` in this package, modified to call the correct local model.

run like 

```
pipetask run -j 4 -p DRPRBAfterburner.yaml -b /repo/main -i LSSTComCam/runs/DRP/20241101_20241120/w_2024_47/DM-47746 -o u/ebellm/w_2024_47/tac_cnn_drp_v2
```

## AP

Running on an ap verify test dataset:

Modify `pipelines/ApVerifyCNN.yaml` to reflect the correct instrument and local model package.


`setup -kr meas_transient`


`setup -kr ap_verify_ci_cosmos_pdr2`


```
ap_verify.py --dataset ap_verify_ci_cosmos_pdr2 --data-query "visit = 59134 AND detector=5" --output test_runs/cosmos_tac_cnn_2025-02-18/ --pipeline ApVerifyCNN.yaml
```
