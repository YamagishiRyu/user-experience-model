# Souce Code
We use Python for scene detection, inference and evaluation, and Golang for batch data processing.  

## Environment
### Python
We use pipenv for virtual environment.  
Inference and evaluation uses Python 3.8.  
Scene detection uses Python 2.7.  

### Golang
We use Golang for data processing such as filtering for CSV, create bag of words.  
Golang version is 15.2. 

## Code
### Batch data processing
Directory: `batch/`. 
This is code for csv data processing.

1. Create Scene Detection Result Data (create_sightseeing_dataset.go)
This collect needed information for user-experience model inference.

2. Create bag of words (create_bag_for_sightseeing.go)
This code indexes uses, locations and words from scene detection result data.  

3. Create geomf input data (create_kyoto_data_for_geomf.go, create_data_for_geomf.go)
These codes create input data for each dataset for GeoMF++ Matlab program.
Data format details [here](https://github.com/DefuLian/recsys#data-preprocessing).


### Scene Detection
Directory: `scene_detection/`.  
Scene detection applies all images for all cities.  
You must prepare flickr data for this.   
This program upload raw image and detected result image to S3.  
You have to put profile and bucket to `.env`.

You can run program at this root directory like this.
```sh
$ pipenv run python scene_detection/detect_sightseeing_all.py
```

### Inference
Directory: `learning/`.  
Inference Program uses [Pyro](https://github.com/pyro-ppl/pyro). 
Pyro version must be `1.3.1`.  
This code uses [Comet](https://www.comet.ml/site/) for experiment management, Slack as notification and AWS S3 to save posterior distribution.  
You have to put api key to `.env`.  
This program needs ID collection file.  
You can run both B-UEM and ST-UEM models.

You can run program at this root directory like this:
```sh
$ pipenv run python leaning/base_for_sightseeing.py -f ../data/ids/id-Edin.csv
```

You can also run debug model.
```sh
$ pipenv run python leaning/st_for_sightseeing.py -f ../data/ids/id-Kyoto.csv --debug
```

### Evaluation
Directory: `evaluation/`.  
Evaluation program downloads posterior distribution by comet experiment id and calculate precision and recall.

You can run program at this root directory like this:
```sh
$ pipenv run python evaluation/evaluate_sightseeint_location_prediction.py
```
