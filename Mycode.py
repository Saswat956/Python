import hashlib
import json
import pandas as pd

def fetch_attributes(properties, hier, element_dict, cntr, current_node_data_type=None):
    """
    Recursively processes properties in JSON data to build a hierarchical structure of attributes.
    """
    for idx, block in enumerate(properties):
        col_desc = {}
        if 'type' in block:
            cntr += 1
            data_type = block['type']
            data_type = ",".join(data_type) if isinstance(data_type, list) else data_type
            field_identifier = block.get('code', '') or block.get('name', '')

            if not field_identifier:
                raise Exception(f"Both 'code' and 'name' are empty for block: {json.dumps(block)}")
            
            attribute_hierarchy = f"{hier}.{field_identifier}"
            
            if block['type'] in ['document', 'object']:
                # Add document or object to hierarchy
                hash_str = hashlib.md5(attribute_hierarchy.encode('utf-8')).hexdigest()
                element_dict[hash_str] = ['Object', 'Parent', attribute_hierarchy, cntr, {}]
                if 'properties' in block:
                    fetch_attributes(block['properties'], attribute_hierarchy, element_dict, cntr, current_node_data_type)

            elif block['type'] == 'array':
                # Add array object to hierarchy
                hash_str = hashlib.md5(attribute_hierarchy.encode('utf-8')).hexdigest()
                element_dict[hash_str] = ['Object', 'Parent', attribute_hierarchy, cntr, {}]
                if 'properties' in block:
                    fetch_attributes(block['properties'], attribute_hierarchy, element_dict, cntr, current_node_data_type=data_type)

            else:
                # Add column to hierarchy
                hash_str = hashlib.md5(attribute_hierarchy.encode('utf-8')).hexdigest()
                col_desc['description'] = block.get('description', '')
                col_desc['active_indicator'] = block.get('isActivated', False)
                col_desc['pii_indicator'] = block.get('piiIn', '')
                col_desc['primary_key_indicator'] = block.get('primaryKey', False)
                col_desc['data_type_name'] = data_type
                col_desc['column_length_number'] = block.get('maxLength', '')
                element_dict[hash_str] = ['Column', 'Leaf', attribute_hierarchy, cntr, col_desc]
    return


def process_hackolade_data(inp_transform, db_nm):
    """
    Processes the top-level structure in the JSON file to build hierarchical metadata.
    """
    element_dict = {}
    cntr = 0

    # Add database and schema
    top_hierarchy = db_nm
    hash_str = hashlib.md5(top_hierarchy.encode('utf-8')).hexdigest()
    element_dict[hash_str] = ['Schema', 'Parent', top_hierarchy, cntr, {}]

    collections = inp_transform.get('collections', [])
    for collection in collections:
        cntr += 1
        collection_name = collection.get('collectionName', '')
        if not collection_name:
            raise Exception("Collection is missing a 'collectionName'.")

        collection_hierarchy = f"{db_nm}.{collection_name}"
        hash_str = hashlib.md5(collection_hierarchy.encode('utf-8')).hexdigest()
        element_dict[hash_str] = ['Object', 'Parent', collection_hierarchy, cntr, {}]

        # Process collection properties
        properties = collection.get('properties', [])
        if not properties:
            raise Exception(f"Collection '{collection_name}' has no properties defined.")

        fetch_attributes(properties, collection_hierarchy, element_dict, cntr)

    # Build a sorted list of elements for easier processing
    entity_list = [
        [k, v[0], v[1], v[2], v[4]] for k, v in element_dict.items()
    ]
    entity_list_sorted = sorted(entity_list, key=lambda x: x[3])  # Sort by hierarchy
    
    return entity_list_sorted


if __name__ == "__main__":
    # Input file path
    data = r"/Users/saswatswain/Downloads/HR assistant/myfile.json"

    with open(data, mode='r') as file_in:
        inp_transform = json.load(file_in)

    # Process JSON
    attribute_list = process_hackolade_data(inp_transform, "GO2")

    # Print and save results
    for idx, node_list in enumerate(attribute_list):
        print(idx, node_list)

    # Save to CSV
    df = pd.DataFrame(attribute_list, columns=['Hash', 'Type', 'Role', 'Hierarchy', 'Metadata'])
    output_path = r"/Users/saswatswain/Downloads/HR assistant/myfile.csv"
    df.to_csv(output_path, index=False)
