import xml.etree.ElementTree as ET


def get_namespaces(xml_file):
    events = "start", "start-ns"
    namespaces = {}
    for event, elem in ET.iterparse(xml_file, events):
        if event == "start-ns":
            prefix, uri = elem
            namespaces[prefix if prefix else 'default'] = uri
        elif event == "start":
            break
    return namespaces


def switch_points(xml_file, output_file):
    namespaces = get_namespaces(xml_file)

    nsmap = {k: v for k, v in namespaces.items()}

    tree = ET.parse(xml_file)
    root = tree.getroot()

    ns_drill_plan = nsmap.get('default')
    ns_ir = nsmap.get('IR')

    for hole in root.findall(f'.//{{{ns_drill_plan}}}Hole'):
        for point in ['StartPoint', 'EndPoint']:
            point_elem = hole.find(f'{{{ns_drill_plan}}}{point}')
            if point_elem is not None:
                point_x = point_elem.find(f'{{{ns_ir}}}PointX')
                point_y = point_elem.find(f'{{{ns_ir}}}PointY')
                if point_x is not None and point_y is not None:
                    original_x = point_x.text
                    original_y = point_y.text
                    point_x.text = original_y
                    point_y.text = original_x

    ET.register_namespace('', ns_drill_plan)
    ET.register_namespace('IR', ns_ir)

    tree.write(output_file, encoding='utf-8', xml_declaration=True)
