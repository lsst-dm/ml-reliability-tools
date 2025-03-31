
from the 2025-02-20 RB model update

### ap_verify datasets

What I want to do is to start is injest the new, local model package into an ap_verify-created butler.

create local model package and set up meas_transinet.


rb/ingest_taccnn_250218.py
```
from lsst.meas.transiNet.modelPackages.nnModelPackage import NNModelPackage
from lsst.meas.transiNet.modelPackages.storageAdapterButler import StorageAdapte
rButler

from lsst.daf.butler import Butler
butler = Butler("./test_runs/cosmos_tac_cnn_2025-02-18/repo/", writeable=True)
local_model_package = NNModelPackage('tac_cnn_comcam_2025-02-18', 'local')
StorageAdapterButler.ingest(local_model_package, butler)
```

having run that, the ap_verify repo now has a copy of in repo/pretrained_models.

now we go to the ci dataset for cosmos, git pull on main, and make a ticket branch (tickets/DM-48748)

in scripts, 
```
python get_nn_models.py \
-b /sdf/home/e/ebellm/u/workspace/rb/test_runs/cosmos_tac_cnn_2025-02-18/repo/ \
-m tac_cnn_comcam_2025-02-18
./make_preloaded_export.py
```

and commit everything (including adding the new directory in pretrained models).  But be careful not to commit .lfsconfig

repeat for dc2 and hits

### ingest into /repo/main etc.

create, update, and run
ingest_main_taccnn_250218.py

once again I get permission denied on /repo/main and dc2

```
butler query-collections embargo_new pretrained* --chains=tree

```

```
butler collection-chain embargo pretrained_models pretrained_models/tac_cnn_comcam_2025-02-18
```

so embargo is right, now let's see if we can transfer to /repo/main

```
butler transfer-datasets embargo /repo/main --dataset-type pretrainedModelPackage --collections pretrained_models/tac_cnn_comcam_2025-02-18 
butler transfer-datasets embargo /repo/dc2 --dataset-type pretrainedModelPackage --collections pretrained_models/tac_cnn_comcam_2025-02-18 
```

nope, I still get permission denied
[fixed](https://rubin-obs.slack.com/archives/C07QM71HQ68/p1740162453676829?thread_ts=1704744671.524439&cid=C07QM71HQ68) next day

(Maybe I will leave the DC2 weights as-is for the DC2 repo since they were at least trained on DC2?  I at least transferred it, but left the old one chained)

however, since embargo is right I can proceed to the DRP datasets


### ingest into ci_hsc_gen3 and ci_imsim

make ticket branches for ci_hsc_gen3 and testdata_ci_hsc

run

```
import lsst.daf.butler as dafButler
butler = dafButler.Butler("embargo")
with butler.export(directory='.', filename='external_pretrained_models.yaml', transfer='copy') as exporter:
    exporter.saveDatasets(butler.query_datasets('pretrainedModelPackage', collections='pretrained_models'))
```

in some directory

git rm the existing pretrained_models in testdata_ci_hsc/pretrained_models and copy in the new one from the directory created by the above

then copy the external_pretrained_models.yaml to /resources in ci_hsc_gen3
change the collection name to HSC/external


repeat for ci_imsim, but this time also edit the defaults chained collection in external.yaml to the new name
