"""
This module include read_kved, write_kved and parse_kved_functions
"""
import json

def read_kved(path: str) -> dict:
    """
    Reads json kved and returns it
    """
    with open(path, encoding='utf-8') as loaded_file:
        return json.load(loaded_file)


def parse_kved(class_code: str) -> None:
    """
    Iterates through kved objects and finds required kved using class_code
    """
    kved = {}
    parent_key = 'parent'
    found_kved = False
    data = read_kved("kved.json")

    sections = data['sections'][0]
    for section in sections:
        divisions = section['divisions']
        for division in divisions:
            groups = division['groups']
            for group in groups:
                classes = group['classes']
                for c_l in classes:
                    if c_l['classCode'] == class_code:
                        kved['name'] = c_l['className']
                        kved['type'] = 'class'
                        found_kved = True
                        break
                if found_kved:
                    kved[parent_key] = {
                        'name': group['groupName'],
                        'type': 'group',
                        'num_children': len(classes)
                    }
                    break
            if found_kved:
                kved[parent_key][parent_key] = {
                    'name': division['divisionName'],
                    'type': 'division',
                    'num_children': len(groups)
                }
                break
        if found_kved:
            kved[parent_key][parent_key][parent_key] = {
                'name': section['sectionName'],
                'type': 'section',
                'num_children': len(divisions)
            }
            break

    with open('kved_results.json', 'w', encoding='utf-8') as loaded_file:
        json_string = json.dumps(kved, ensure_ascii=False)
        loaded_file.write(json_string)
