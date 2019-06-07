# ACE2005 preprocessing

This is a simple code for preprocessing ACE 2005 corpus for Event Extraction task.



## Usage


1. Prepare **ACE 2005 dataset** 

   (Download: https://catalog.ldc.upenn.edu/LDC2006T06. Note that ACE 2005 dataset is not free.)

2. Run:

    ```bash
    python main.py --data=./data/ace_2005_td_v7/data/English
    ```
    
    Then you can get parsed test/dev/train data in `output folder`.
    ```
    ├── output
    │     └── test.json
    │     └── dev.json
    │     └── train.json
    │...
    ```
    
    
## Output

The results are generated in json format, like this sample. 

If you want to know event types and arguments in detail, read [this document (ACE 2005 event guidelines)](https://www.ldc.upenn.edu/sites/www.ldc.upenn.edu/files/english-events-guidelines-v5.4.3.pdf).

### Sample
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
    "golden_event_mention": {
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
    }
}]
```

### Statistic

