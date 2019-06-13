import os
from parser import Parser
import json
import argparse


def get_data_paths(ace2005_path):
    test_files, dev_files, train_files = [], [], []

    with open('./data_list.csv', mode='r') as csv_file:
        rows = csv_file.readlines()
        for row in rows[1:]:
            items = row.replace('\n', '').split(',')
            data_type = items[0]
            name = items[1]

            path = os.path.join(ace2005_path, name)
            if data_type == 'test':
                test_files.append(path)
            elif data_type == 'dev':
                dev_files.append(path)
            elif data_type == 'train':
                train_files.append(path)
    return test_files, dev_files, train_files


def preprocessing(data_type, files):
    data = []

    event_count, entity_count, sent_count = 0, 0, 0

    for file in files:
        parser = Parser(path=file)
        data.extend(parser.get_data())

        entity_count += len(parser.entity_mentions)
        event_count += len(parser.event_mentions)
        sent_count += len(parser.sents_with_pos)

    print('[result] type: ', data_type)
    print('sent_count :', sent_count)
    print('event_count :', event_count)
    print('entity_count :', entity_count)

    with open('output/{}.json'.format(data_type), 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help="Path of ACE2005 English data", default='./data/ace_2005_td_v7/data/English')
    args = parser.parse_args()
    test_files, dev_files, train_files = get_data_paths(args.data)
    preprocessing('test', test_files)
    preprocessing('train', train_files)
    preprocessing('dev', dev_files)

    # from stanfordcorenlp import StanfordCoreNLP
    #
    # nlp = StanfordCoreNLP('./stanford-corenlp-full-2018-10-05')
    # print('loaded!')
    # print(nlp.annotate('Thousands of fresh US troops headed for Iraq Thursday as British Prime Minister Tony Blair and US President George W. Bush discussed the effort to oust Saddam Hussein, which some senior US military officials warn could last months.', properties={'annotators': 'ssplit'}))
    # nlp.close()
