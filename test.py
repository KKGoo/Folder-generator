import json
import os


def file_gen(data, path, name):

    jsonString = json.dumps(
        data, indent=2, separators=(',', ': '), sort_keys=True)
    jsonFile = open(f"{path}/{name}.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()


def json_gen(blocks_file, block_component, block_data, blocks_key, data_type):
    if not blocks_key in blocks_file:
        return
    if not data_type in blocks_file[blocks_key]:

        return
    for block in blocks_file[blocks_key][data_type]:
        if not blocks_key in block_data:
            block_data[blocks_key] = {data_type: []}
        block_data[blocks_key][data_type].append(block)
        json_gen(blocks_file, block_component, block_data, block, 'children')
        if block in blocks_file:
            if not block in block_component:
                block_component[block] = blocks_file[block]          
    block_data = {**block_data,**block_component}
    return block_data


def folder_gen(parent, routes_file, blocks_file):
    if not "screens" in routes_file:
        return
    keys = routes_file["screens"].keys()
    blocks_file
    for key in keys:
        data_child = routes_file["screens"][key]
        route_path = f"{parent}/{key}"
        path = os.path.join(route_path)
        os.makedirs(path)
        prop = data_child.copy()
        if "screens" in prop:
            prop.pop("screens")
        if "Component" == data_child['type']:
            blocks_key = f"store.{key}"
            block_data = {blocks_key: {'blocks': []}}
            block_component = {}
            block_data = json_gen(
                blocks_file, block_component, block_data, blocks_key, 'blocks')
            if block_data:
                file_gen(block_data, path, 'blocks')
        file_gen(prop, path, 'props')
        folder_gen(route_path, data_child, blocks_file)


if __name__ == "__main__":
    file = open('routes.json')
    routes_file = json.load(file)
    blocks = open('blocks.json')
    blocks_file = json.load(blocks)
    folder_gen("./routes", routes_file, blocks_file)
