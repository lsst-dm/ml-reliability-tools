
# Generating png and numpy cutouts

## DRP

`drp_cutouts.py` script is in the `bin` directory of this repo

```
./bin/drp_cutouts.py /repo/main --collections=LSSTComCam/runs/DRP/DP1/w_2025_09/DM-49235  -o /sdf/group/rubin/shared/notebooks/real_bogus/some_output_dir -j6  --not-injected  --where "detector=4 and visit=2024112800140 and instrument='LSSTComCam'"
```

use `./bin/drp_cutouts --help` to see arguments; note particularly `--injected` vs `--not-injected`.	


## AP

see [here](https://pipelines.lsst.io/v/daily/modules/lsst.analysis.ap/scripts/plotImageSubtractionCutouts.html#plotimagesubtractioncutouts) for arguments.

```
plotImageSubtractionCutouts embargo_new . --sqlitefile /sdf/home/b/bos/u/DM-47227/apdb_LSSTComCam_DM-47227_v6.sqlite -C configs_with_fakes --collections u/bos/ComCam/APWithFakes/DM-47227/LSSTComCam_ApPipeWithFakes_v6 --instrument LSSTComCam  --all -j 5 --limit 5000
```

