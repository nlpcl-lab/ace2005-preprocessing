# ACE2005 preprocessing

This is a simple code for preprocessing ACE 2005 corpus for Event Extraction task. 

Using the existing methods were complicated for me, so I made this project.

## Prerequisites

1. Prepare **ACE 2005 dataset**. 

   (Download: https://catalog.ldc.upenn.edu/LDC2006T06. Note that ACE 2005 dataset is not free.)

2. Install the packages.
   ```
   pip install stanfordcorenlp beautifulsoup4 nltk tqdm
   ```
    
3. Download stanford-corenlp model.
    ```bash
    wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip
    unzip stanford-corenlp-full-2018-10-05.zip
    ```

## Usage

Run:

```bash
sudo python main.py --data=./data/ace_2005_td_v7/data/English --nlp=./stanford-corenlp-full-2018-10-05
``` 

- Then you can get the parsed data in `output directory`. 

- If it is not executed with the `sudo`, an error can occur when using `stanford-corenlp`.

- It takes about 30 minutes to complete the pre-processing.

## Output

### Format

I follow the json format described in
[EMNLP2018-JMEE](https://github.com/lx865712528/EMNLP2018-JMEE)
repository like the bellow sample. Furthermore, I add entity head for
each entity, because many nlp tasks exploit the head of entity not the
mention of entity.

If you want to know event types and arguments in detail, read [this document (ACE 2005 event guidelines)](https://www.ldc.upenn.edu/sites/www.ldc.upenn.edu/files/english-events-guidelines-v5.4.3.pdf).


**`sample.json`**
```json
[
    {
    "sentence": "Earlier documents in the case have included embarrassing details about perks Welch received as part of his retirement package from GE at a time when corporate scandals were sparking outrage.",
    "golden-entity-mentions": [
      {
        "text": "Welch",
        "entity-type": "PER:Individual",
        "head": {
          "text": "Welch",
          "start": 11,
          "end": 12
        },
        "entity_id": "APW_ENG_20030325.0786-E24-38",
        "start": 11,
        "end": 12
      },
      {
        "text": "his",
        "entity-type": "PER:Individual",
        "head": {
          "text": "his",
          "start": 16,
          "end": 17
        },
        "entity_id": "APW_ENG_20030325.0786-E24-39",
        "start": 16,
        "end": 17
      },
      {
        "text": "GE",
        "entity-type": "ORG:Commercial",
        "head": {
          "text": "GE",
          "start": 20,
          "end": 21
        },
        "entity_id": "APW_ENG_20030325.0786-E26-40",
        "start": 20,
        "end": 21
      }
    ],
    "golden-event-mentions": [
      {
        "trigger": {
          "text": "retirement",
          "start": 17,
          "end": 18
        },
        "arguments": [
          {
            "role": "Person",
            "entity-type": "PER:Individual",
            "text": "Welch",
            "start": 11,
            "end": 12
          },
          {
            "role": "Entity",
            "entity-type": "ORG:Commercial",
            "text": "GE",
            "start": 20,
            "end": 21
          }
        ],
        "event_type": "Personnel:End-Position"
      }
    ],
    "stanford-colcc": [
      "ROOT/dep=6/gov=-1",
      "amod/dep=0/gov=1",
      "nsubj/dep=1/gov=6",
      "case/dep=2/gov=4",
      "det/dep=3/gov=4",
      "nmod:in/dep=4/gov=1",
      "aux/dep=5/gov=6",
      "amod/dep=7/gov=8",
      "dobj/dep=8/gov=6",
      "case/dep=9/gov=10",
      "nmod:about/dep=10/gov=6",
      "nsubj/dep=11/gov=12",
      "acl:relcl/dep=12/gov=10",
      "case/dep=13/gov=14",
      "nmod:as/dep=14/gov=12",
      "case/dep=15/gov=18",
      "nmod:poss/dep=16/gov=18",
      "compound/dep=17/gov=18",
      "nmod:of/dep=18/gov=14",
      "case/dep=19/gov=20",
      "nmod:from/dep=20/gov=12",
      "case/dep=21/gov=23",
      "det/dep=22/gov=23",
      "nmod:at/dep=23/gov=12",
      "advmod/dep=24/gov=28",
      "amod/dep=25/gov=26",
      "nsubj/dep=26/gov=28",
      "aux/dep=27/gov=28",
      "acl:relcl/dep=28/gov=23",
      "dobj/dep=29/gov=28",
      "punct/dep=30/gov=6"
    ],
    "words": [
      "Earlier",
      "documents",
      "in",
      "the",
      "case",
      "have",
      "included",
      "embarrassing",
      "details",
      "about",
      "perks",
      "Welch",
      "received",
      "as",
      "part",
      "of",
      "his",
      "retirement",
      "package",
      "from",
      "GE",
      "at",
      "a",
      "time",
      "when",
      "corporate",
      "scandals",
      "were",
      "sparking",
      "outrage",
      "."
    ],
    "pos-tags": [
      "JJR",
      "NNS",
      "IN",
      "DT",
      "NN",
      "VBP",
      "VBN",
      "JJ",
      "NNS",
      "IN",
      "NNS",
      "NNP",
      "VBD",
      "IN",
      "NN",
      "IN",
      "PRP$",
      "NN",
      "NN",
      "IN",
      "NNP",
      "IN",
      "DT",
      "NN",
      "WRB",
      "JJ",
      "NNS",
      "VBD",
      "VBG",
      "NN",
      "."
    ],
    "lemma": [
      "earlier",
      "document",
      "in",
      "the",
      "case",
      "have",
      "include",
      "embarrassing",
      "detail",
      "about",
      "perk",
      "Welch",
      "receive",
      "as",
      "part",
      "of",
      "he",
      "retirement",
      "package",
      "from",
      "GE",
      "at",
      "a",
      "time",
      "when",
      "corporate",
      "scandal",
      "be",
      "spark",
      "outrage",
      "."
    ],
    "parse": "(ROOT\n  (S\n    (NP\n      (NP (JJR Earlier) (NNS documents))\n      (PP (IN in)\n        (NP (DT the) (NN case))))\n    (VP (VBP have)\n      (VP (VBN included)\n        (NP (JJ embarrassing) (NNS details))\n        (PP (IN about)\n          (NP\n            (NP (NNS perks))\n            (SBAR\n              (S\n                (NP (NNP Welch))\n                (VP (VBD received)\n                  (PP (IN as)\n                    (NP\n                      (NP (NN part))\n                      (PP (IN of)\n                        (NP (PRP$ his) (NN retirement) (NN package)))))\n                  (PP (IN from)\n                    (NP (NNP GE)))\n                  (PP (IN at)\n                    (NP\n                      (NP (DT a) (NN time))\n                      (SBAR\n                        (WHADVP (WRB when))\n                        (S\n                          (NP (JJ corporate) (NNS scandals))\n                          (VP (VBD were)\n                            (VP (VBG sparking)\n                              (NP (NN outrage)))))))))))))))\n    (. .)))"
  }
]
```


### Data Split

The result of data is divided into test/dev/train as follows.
```
├── output
│     └── test.json
│     └── dev.json
│     └── train.json
│...
```

This project use the same data partitioning as the previous work ([Yang and Mitchell, 2016](https://www.cs.cmu.edu/~bishan/papers/joint_event_naacl16.pdf);  [Nguyen et al., 2016](https://www.aclweb.org/anthology/N16-1034)). The data segmentation is specified in `data_list.csv`.

Below is information about the amount of parsed data when using this project. It is slightly different from the parsing results of the two papers above. The difference seems to have occurred because there are no promised rules for splitting sentences within the sgm format files.

|          | Documents    |  Sentences   |Triggers    | Arguments | Entity Mentions  |
|-------   |--------------|--------------|------------|-----------|----------------- |
| Test     | 40        | 713           | 422           | 892             |  4226             |
| Dev      | 30        | 875           | 492           | 933             |  4050             |
| Train    | 529       | 14724         | 4312          | 7811             |   53045            |
