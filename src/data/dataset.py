from xml.etree import ElementTree as ET
import re

def remove_http_text(xml_tag: str):
    """Remove http text inside curly braces from an XML tag."""
    return re.sub(r'\{http.*?\}', '', xml_tag)

def xml_to_dict_rec(root: ET.Element):
    """Recursively convert an XML element to a dictionary."""
    data = {}
    for child in root:
        # Skip tags related to metadata and formatting
        if child.tag.startswith('{http://tcga.nci/bcr/xml/administration/2.7}'):
            continue

        # Recursive call for child elements
        child_data = xml_to_dict_rec(child)

        child_tag = remove_http_text(child.tag)

        # Handle multiple child elements with the same tag
        if child_tag in data:
            if not isinstance(data[child_tag], list):
                data[child_tag] = [data[child_tag]]
            data[child_tag].append(child_data)
        else:
            data[child_tag] = child_data

    if data:
        return data

    return root.text.strip() if root.text else ''

def xml_to_dict(xml_path: str):
    """ Convert an XML file to a dictionary.

    Args:
        xml_path (str): Path to an XML file.

    Returns:
        dict: Dictionary representation of the XML file.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    return xml_to_dict_rec(root)

def make_dataset():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).

        Processing steps:
        1. RNA-seq data:
            1.1. Match RNA-seq profiles with clinical data.
            1.2. Where there are multiple profiles for a single patient,
                retain the profile with the highest mean expression.
            1.3. Remove genes that are not either protein-coding or lncRNA.
        2. Clinical data:
            1.1. Parse XML files into a dictionary.
            1.2. Remove fields that won't be used, enforce data types, and rename fields.
    """
