from xml.etree import ElementTree


class Parser:
    def __init__(self, xml_path):
        self.entity_mentions = []
        self.event_mentions = []

        self.parse(xml_path)

    def get_data(self):
        pass

    def parse(self, xml_path):
        tree = ElementTree.parse(xml_path)
        root = tree.getroot()

        for child in root[0]:
            if child.tag == 'entity':
                self.entity_mentions.extend(self.parse_entity_tag(child))
            elif child.tag in ['value', 'timex2']:
                self.entity_mentions.extend(self.parse_value_timex(child))
            elif child.tag == 'event':
                self.event_mentions.extend(self.parse_event_tag(child))

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
