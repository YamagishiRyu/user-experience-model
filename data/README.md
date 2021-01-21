# Dataset
We use two kinds of dataset.
- Flickr Kyoto
- User Visits dataset

Both dataset is collected from Flickr [YFCC100M](https://dl.acm.org/doi/abs/10.1145/2812802).
We filtered YFCC100M to data in Kyoto-shi for Flickr Kyoto.
User Visit dataset is [public dataset](https://sites.google.com/site/limkwanhui/datacode#h.p_ID_65) which K.H.Lim created from YFCC100M.

This directory includes some kinds of data.
- Flicker
- Scene Detection Result
- ID collection for inference
- Bag of Words
- GeoMF++ input data

## Flickr
Directory: `flickr/`
This is the data from Flickr for each dataset.
All data has their photo (It does not lose link in 2020/11) and you can download image by their Photo/video download URL.

## Scene Detection Result
Directory: `./`
We detect scenes for each image and collect key data for leaning for each city(exclude Kyoto).
Key data if below:
- photo identifier
- user identifier
- time
- location identifier
- some words describing behaviors
All data are used as discrete distribution.
The number of words for each image must be the same.

## ID collection for inference
Directory: `ids/`
This data is output for indexing scene detection result.

## Bag of Words
Directory: `bags/`
This data is sub output for indexing scene detection result. 
This includes index for user, location, word.

## GeoMF++ input data
Directory: `geomf/`
This is dataset for GeoMF++.
This dataset follows [rules](https://github.com/DefuLian/recsys#data-preprocessing) and includes user identifier, location identifier, visit count.
