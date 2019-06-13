import os
from parser import Parser
import json
from stanfordcorenlp import StanfordCoreNLP
import argparse
from tqdm import tqdm


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


def find_token_index(tokens, start_pos, end_pos):
    start_idx, end_idx = -1, -1
    for idx, token in enumerate(tokens):
        if token['characterOffsetBegin'] <= start_pos:
            start_idx = idx
        if token['characterOffsetEnd'] == end_pos:
            end_idx = idx

    # Some of the ACE2005 data has annotation position error.
    if end_idx == -1:
        end_idx = start_idx

    return start_idx, end_idx


def preprocessing(data_type, files):
    result = []
    event_count, entity_count, sent_count = 0, 0, 0

    print('-' * 20)
    print('[preprocessing] type: ', data_type)
    for file in tqdm(files):
        parser = Parser(path=file)

        entity_count += len(parser.entity_mentions)
        event_count += len(parser.event_mentions)
        sent_count += len(parser.sents_with_pos)

        for item in parser.get_data():
            data = dict()
            data['sentence'] = item['sentence']
            data['golden_entity_mentions'] = []
            data['golden_event_mentions'] = []
            data['position'] = item['position']

            nlp_res = nlp.annotate(item['sentence'], properties={'annotators': 'tokenize,ssplit,pos,parse'})
            nlp_res = json.loads(nlp_res)

            tokens = nlp_res['sentences'][0]['tokens']
            # data['nlp_tokens'] = tokens

            data['tokens'] = list(map(lambda x: x['word'], tokens))
            data['pos-tag'] = list(map(lambda x: x['pos'], tokens))
            data['parse'] = nlp_res['sentences'][0]['parse']

            sent_start_pos = item['position'][0]

            for entity_mention in item['golden_entity_mentions']:
                position = entity_mention['position']
                start_idx, end_idx = find_token_index(tokens, position[0] - sent_start_pos, position[1] - sent_start_pos + 1)

                entity_mention['start'] = start_idx
                entity_mention['end'] = end_idx

                del entity_mention['position']

                data['golden_entity_mentions'].append(entity_mention)

            for event_mention in item['golden_event_mentions']:
                position = event_mention['trigger']['position']
                start_idx, end_idx = find_token_index(tokens, position[0] - sent_start_pos, position[1] - sent_start_pos + 1)

                event_mention['trigger']['start'] = start_idx
                event_mention['trigger']['end'] = end_idx
                del event_mention['trigger']['position']
                del event_mention['position']

                data['golden_event_mentions'].append(event_mention)

            result.append(data)

    print('sent_count :', sent_count)
    print('event_count :', event_count)
    print('entity_count :', entity_count)

    with open('output/{}.json'.format(data_type), 'w') as f:
        json.dump(result, f, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help="Path of ACE2005 English data", default='./data/ace_2005_td_v7/data/English')
    args = parser.parse_args()
    test_files, dev_files, train_files = get_data_paths(args.data)

    nlp = StanfordCoreNLP('./stanford-corenlp-full-2018-10-05')
    preprocessing('test', test_files)
    # preprocessing('train', train_files)
    # preprocessing('dev', dev_files)
    nlp.close()
