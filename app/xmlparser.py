import xml.etree.ElementTree as ET
from datetime import date


def xml_to_dict(file_path, remains=True, reverse=False):
    tree = ET.parse(file_path)
    root = tree.getroot()
    info = []

    for child in root:
        dict = {k.tag: k.text for k in child}
        if remains:
            dict['remains'] = count_remains(dict)
            if reverse:
                dict['remains'] = - count_remains(dict)
            try:
                dict['last'] = int(dict['last'])
            except KeyError:
                pass
        info.append(dict)
    if remains:
        info.sort(key=sort_by_value)
    return info


def sort_by_value(value):
    return value['remains']


def count_remains(dict):
    ddl = date(int(dict['year']), int(dict['month']), int(dict['day']))
    today = date.today()
    return (ddl - today).days


def delete_element(filename, name):
    tree = ET.parse('app/xmls/{}'.format(filename))
    root = tree.getroot()
    for child in root.findall('event'):
        if child.find('name').text == name:
            root.remove(child)
    tree.write('app/xmls/{}'.format(filename))


def add_new(filepath, data):
    tree = ET.parse(filepath)
    root = tree.getroot()
    event = ET.SubElement(root, 'event')
    for key, value in data.items():
        sub = ET.SubElement(event, key)
        sub.text = str(value)
    tree.write(filepath)


def daily_update(filename, name, undo=False):
    tree = ET.parse('app/xmls/{}'.format(filename))
    root = tree.getroot()
    for child in root.findall('event'):
        if child.find('name').text == name:
            if undo:
                child.find('last').text = str(int(child.find('last').text) - 1)
            else:
                child.find('last').text = str(int(child.find('last').text) + 1)
    tree.write('app/xmls/{}'.format(filename))

