import xml.etree.ElementTree as ET
import csv


def get_namespaces(xml_file):
    events = "start", "start-ns"
    namespaces = {}
    for event, elem in ET.iterparse(xml_file, events):
        if event == "start-ns":
            prefix, uri = elem
            namespaces[prefix] = uri
        elif event == "start":
            break
    return namespaces


def xml_to_csv_period(xml_file, csv_file):
    namespaces = get_namespaces(xml_file)

    tree = ET.parse(xml_file)
    root = tree.getroot()

    default_ns = namespaces.get('')

    if default_ns:
        xpath_query = f".//{{{default_ns}}}CgPoints/{{{default_ns}}}CgPoint"
    else:
        xpath_query = ".//CgPoints/CgPoint"

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')

        for cgpoint in root.findall(xpath_query):
            name = cgpoint.attrib.get('name', '')
            coordinates = cgpoint.text.strip()

            coordinate_list = coordinates.split()

            row = [name] + coordinate_list

            writer.writerow(row)


def xml_to_csv_comma(xml_file, csv_file):
    namespaces = get_namespaces(xml_file)

    tree = ET.parse(xml_file)
    root = tree.getroot()

    default_ns = namespaces.get('')

    if default_ns:
        xpath_query = f".//{{{default_ns}}}CgPoints/{{{default_ns}}}CgPoint"
    else:
        xpath_query = ".//CgPoints/CgPoint"

    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')

        for cgpoint in root.findall(xpath_query):
            name = cgpoint.attrib.get('name', '')
            coordinates = cgpoint.text.strip()

            coordinate_list = coordinates.split()

            coordinate_list_comma = [coord.replace(
                '.', ',') for coord in coordinate_list]

            row = [name] + coordinate_list_comma

            writer.writerow(row)
