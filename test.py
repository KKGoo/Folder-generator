import json
import os


def file_gen(data, path, name) : 
    """
    > This function takes in a dictionary, a path, and a name, and writes the dictionary to a json file
    in the specified path with the specified name. 
    
    Let's try it out. 
    
    First, let's create a dictionary.
    
    :param data: The data to be written to the file
    :param path: The path to the directory where you want to save the file
    :param name: The name of the file
    """
    jsonString = json.dumps(data, indent=2, separators=(',', ': '), sort_keys=True)
    jsonFile = open(f"{path}/{name}.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

def json_gen(blocks, key, data_type):
    """
    It takes a dictionary of blocks, a key, and a data type, and returns a dictionary of the blocks
    
    :param blocks: The dictionary that contains all the blocks
    :param key: The name of the block
    :param data_type: This is the type of data that you want to get from the blocks
    :return: A dictionary that contains the data of the blocks.
    """
    if not key in blocks:
        return
    if not data_type in blocks[key]:
        return
    block_data = {key: {"children": []}}
    for block in blocks[key][data_type]:
        # A dictionary that is being created to store the data of the blocks.
        children = json_gen(blocks, block, "children")
        if children:
            block_data[key]["children"].append(children)
        else:
            block_data[key]["children"].append(block)
        #print({key: {data_type: block}})
    return block_data

def folder_gen(parent, data, blocks):
    """
    It takes a parent path, a dictionary of data, and a dictionary of blocks
    
    :param parent: The parent folder path
    :param data: The data from the JSON file
    :param blocks: The blocks dictionary from the JSON file
    :return: The return value is a dictionary with the following keys:
        - "screens": A dictionary of the screens in the project.
        - "blocks": A dictionary of the blocks in the project.
        - "props": A dictionary of the props in the project.
    """
    if not "screens" in data:
        return
    keys = data["screens"].keys()

    for key in keys:
        data_child = data["screens"][key]
        route_path = f"{parent}/{key}"
        path = os.path.join(route_path)
        os.makedirs(path)
        prop = data_child.copy()
        # Removing the screens key from the prop dictionary.
        if "screens" in prop:
            prop.pop("screens")
        if "Component" == data_child['type']:
            blocks_key = f"store.{key}"
            block_data = json_gen(blocks, blocks_key, 'blocks')
            if block_data:
                file_gen(block_data, path, 'blocks')        
            else:
                file_gen(key, path, 'blocks')        
        file_gen(prop, path, 'props')        
        folder_gen(route_path, data_child, blocks)


if __name__ == "__main__":
    file = open('routes.json')
    blocks = open('blocks.json')
    data_blocks = json.load(blocks)
    data = json.load(file)
    folder_gen("./routes", data, data_blocks)
