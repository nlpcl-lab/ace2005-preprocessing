import os
import csv
from config import Config

from xml.etree import ElementTree


def get_files():
    files = list()
    with open('./file_list.csv', mode='r') as csv_file:
        rows = csv_file.readlines()
        for row in rows[1:]:
            items = row.replace('\n', '').split(',')
            files.append({
                'type': items[0],
                'xml_path': os.path.join(Config.ace2005_path, items[1] + '.apf.xml'),
            })
    return files


def parse(xml_path):
    tree = ElementTree.parse(xml_path)
    print(tree)
    root = tree.getroot()
    entities, events = [], []

    for child in root[0]:
        if child.tag == 'entity':
            entities.extend(parse_entity_tag(child))
        elif child.tag in ['value', 'timex2']:
            entities.extend(parse_value_timex(child))
        elif child.tag == 'event':
            events.extend(parse_event_tag(child))
    return entities, events


def parse_entity_tag(node):
    entity_mentions = []

    for child in node:
        if child.tag != 'entity_mention':
            continue
        extent = child[0]
        charset = extent[0]

        entity_mention = dict()
        entity_mention['entity_id'] = child.attrib['ID']
        entity_mention['entity_type'] = '{}:{}'.format(node.attrib['TYPE'], node.attrib['SUBTYPE'])
        entity_mention['text'] = charset.text
        entity_mention['position'] = (int(charset.attrib['START']), int(charset.attrib['END']))

        entity_mentions.append(entity_mention)

    return entity_mentions


def parse_event_tag(node):
    event_mentions = []
    for child in node:
        if child.tag == 'event_mention':
            event_mention = dict()
            event_mention['event_type'] = '{}:{}'.format(node.attrib['TYPE'], node.attrib['SUBTYPE'])
            event_mention['arguments'] = []
            for child2 in child:
                if child2.tag == 'ldc_scope':
                    charset = child2[0]
                    event_mention['text'] = charset.text
                    event_mention['position'] = (int(charset.attrib['START']), int(charset.attrib['END']))
                if child2.tag == 'anchor':
                    charset = child2[0]
                    event_mention['trigger'] = charset.text
                if child2.tag == 'event_mention_argument':
                    extent = child2[0]
                    charset = extent[0]
                    event_mention['arguments'].append({
                        'text': charset.text,
                        'role': child2.attrib['ROLE'],
                        'entity_id': child2.attrib['REFID']
                    })
            event_mentions.append(event_mention)
    return event_mentions


def parse_value_timex(node):
    entity_mentions = []

    for child in node:
        extent = child[0]
        charset = extent[0]

        entity_mention = dict()
        entity_mention['entity_id'] = child.attrib['ID']

        if 'TYPE' in node.attrib:
            entity_mention['entity_type'] = node.attrib['TYPE']
        if 'SUBTYPE' in node.attrib:
            entity_mention['entity_type'] += ':{}'.format(node.attrib['SUBTYPE'])
        if child.tag == 'timex2_mention':
            entity_mention['entity_type'] = 'TIM:time'

        entity_mention['text'] = charset.text
        entity_mention['position'] = (int(charset.attrib['START']), int(charset.attrib['END']))

        entity_mentions.append(entity_mention)

    return entity_mentions


if __name__ == '__main__':
    files = get_files()
    entities, events = parse('./data/ace_2005_td_v7/data/English/nw/timex2norm/AFP_ENG_20030304.0250.apf.xml')
    print(entities)
    print(events)
    pass
