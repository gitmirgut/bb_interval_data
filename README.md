# 1 Setup
```
$ conda create --name map_data python=3
$ source activate map_data
(map_data)$ conda install --channel https://conda.binstar.org/menpo opencv3
(map_data)$ pip install -r requirements.txt
```
# 2 Globale Variablen
Bitte die globalen Variablen, wenn nötig in der Datei [2016_Cams_01_map_all_binaries.py](./2016_Cams_01_map_all_binaries.py) anpassen:

```
PATH_REPRO_IN = '/mnt/storage/beesbook-data-clean/pipeline_data/repo_season_2016_fixed'
PATH_REPRO_OUT = '/mnt/storage/beesbook/171109_mapped_repo_season_2016_fixed'
PATH_INTERVALS = './2016_Cams_01_intervals_pair_validation.json'
PATH_PARAM = './2016_Cams01/'
LOG_PATH = '2016_Cams01_log.txt'
CAM_LEFT = 0
CAM_RIGHT = 1`
```
# 3 Start
```
(map_data)$ python 2016_Cams_01_map_all_binaries.py
```
