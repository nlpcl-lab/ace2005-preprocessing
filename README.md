# ACE2005 preprocessing

This is a simple code for preprocessing ACE 2005 corpus for Event Extraction task.

## Prerequisites

1. Prepare **ACE 2005 dataset** 

   (Download: https://catalog.ldc.upenn.edu/LDC2006T06. Note that ACE 2005 dataset is not free.)

2. Install the stanfordcorenlp package.
   ```
   pip install stanfordcorenlp beautifulsoup4 nltk
   ```
    
3. Download stanfordcorenlp model.
    ```bash
    wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip
    unzip stanford-corenlp-full-2018-10-05.zip
    ```

## Usage

Run:

```bash
python main.py --data=./data/ace_2005_td_v7/data/English
``` 
Then you can get the parsed data in `output directory`. 

## Output

### Format

The results are generated in json format, like the bellow sample.

If you want to know event types and arguments in detail, read [this document (ACE 2005 event guidelines)](https://www.ldc.upenn.edu/sites/www.ldc.upenn.edu/files/english-events-guidelines-v5.4.3.pdf).


**`sample.json`**
```json
[{
    "sentence": "He visited all their families",
    "golden_entity_mentions": [
      {
        "text": "He",
        "entity_type": "PER:Individual"
      },
      {
        "text": "their",
        "entity_type": "PER:Group"
      },
      {
        "text": "all their families",
        "entity_type": "PER:Group"
      }
    ],
    "golden_event_mentions": [{
      "trigger": "visited",
      "arguments": [
        {
          "role": "Entity",
          "entity_type": "PER:Individual",
          "text": "He"
        },
        {
          "role": "Entity",
          "entity_type": "PER:Group",
          "text": "all their families"
        }
      ],
      "event_type": "Contact:Meet"
    }]
}]
```


### Data Split

The resulting data is divided into test/dev/train as follows.
```
├── output
│     └── test.json
│     └── dev.json
│     └── train.json
│...
```

This project use the same data split as the previous work (Liu et al., 2016b; Nguyen et al., 2016). The data segmentation is specified in `data_list.csv`.

Below is information about the amount of data.

|       	| Documents 	| Event Mentions 	| Entity Mensions 	|
|-------	|-----------	|----------------	|-----------------	|
| Test  	| 40        	| 424            	| 4226            	|
| Dev   	| 30        	| 505            	| 4050            	|
| Train 	| 529       	| 4420           	| 53045           	|

