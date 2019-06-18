import os
import copy
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


def find_token_index(tokens, start_pos, end_pos, phrase):
    start_idx, end_idx = -1, -1
    for idx, token in enumerate(tokens):
        if token['characterOffsetBegin'] <= start_pos:
            start_idx = idx
        # if token['characterOffsetEnd'] == end_pos:
        #     end_idx = idx - 1

    # Some of the ACE2005 data has annotation position errors.
    if end_idx == -1:
        end_idx = start_idx + len(phrase.split())

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
            data['golden-entity-mentions'] = []
            data['golden-event-mentions'] = []

            try:
                nlp_text = nlp.annotate(item['sentence'], properties={'annotators': 'tokenize,ssplit,pos,lemma,parse'})
                nlp_res = json.loads(nlp_text)
            except Exception as e:
                print('StanfordCore Exception ', e)
                print('item["sentence"] :', item['sentence'])
                print('nlp_text :', nlp_text)
                continue

            tokens = nlp_res['sentences'][0]['tokens']
            # data['nlp_tokens'] = tokens
            # data['position'] = item['position']

            if len(nlp_res['sentences']) >= 2:
                print('len >=2! Sentence :', data['sentence'])
                # print(nlp_res)
                continue

            data['stanford-colcc'] = []
            for dep in nlp_res['sentences'][0]['enhancedPlusPlusDependencies']:
                data['stanford-colcc'].append('{}/dep={}/gov={}'.format(dep['dep'], dep['dependent'], dep['governor']))

            data['words'] = list(map(lambda x: x['word'], tokens))
            data['pos-tags'] = list(map(lambda x: x['pos'], tokens))
            data['lemma'] = list(map(lambda x: x['lemma'], tokens))
            data['parse'] = nlp_res['sentences'][0]['parse']

            sent_start_pos = item['position'][0]

            for entity_mention in item['golden-entity-mentions']:
                position = entity_mention['position']
                start_idx, end_idx = find_token_index(
                    tokens=tokens,
                    start_pos=position[0] - sent_start_pos,
                    end_pos=position[1] - sent_start_pos + 1,
                    phrase=entity_mention['text'],
                )

                entity_mention['start'] = start_idx
                entity_mention['end'] = end_idx

                del entity_mention['position']

                data['golden-entity-mentions'].append(entity_mention)

            for event_mention in item['golden-event-mentions']:
                # same event mention cab be shared
                event_mention = copy.deepcopy(event_mention)
                position = event_mention['trigger']['position']
                start_idx, end_idx = find_token_index(
                    tokens=tokens,
                    start_pos=position[0] - sent_start_pos,
                    end_pos=position[1] - sent_start_pos + 1,
                    phrase=event_mention['trigger']['text'],
                )

                event_mention['trigger']['start'] = start_idx
                event_mention['trigger']['end'] = end_idx
                del event_mention['trigger']['position']
                del event_mention['position']

                arguments = []
                for argument in event_mention['arguments']:
                    position = argument['position']
                    start_idx, end_idx = find_token_index(
                        tokens=tokens,
                        start_pos=position[0] - sent_start_pos,
                        end_pos=position[1] - sent_start_pos + 1,
                        phrase=argument['text'],
                    )
                    argument['start'] = start_idx
                    argument['end'] = end_idx
                    del argument['position']

                    arguments.append(argument)

                event_mention['arguments'] = arguments
                data['golden-event-mentions'].append(event_mention)

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

    with StanfordCoreNLP('./stanford-corenlp-full-2018-10-05', memory='8g', timeout=30000) as nlp:
        # res = nlp.annotate('Donald John Trump is current president of the United States.', properties={'annotators': 'tokenize,ssplit,pos,lemma,parse'})
        # print(res)
        preprocessing('dev', dev_files)
        preprocessing('train', train_files)
        preprocessing('test', test_files)
