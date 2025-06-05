###################################
#
# @fileoverview Conversion script for xml files that contain MMS messages
#
# @file convert.py
# @date 06-01-2025
# @author Holden Kittelberger
#
###################################

######### IMPORT STATEMENTS #########
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
from tqdm import tqdm

########## FUNCTIONS #########

# strip_namespace 
#
# Purpose: Function to remove XML namespace from tags
# Parameters: The xml tag string to parse and edit
# Returns: The tag string without the namespace and brackets
# Expects: tag is not null
#
def strip_namespace(tag):
    if tag is None:
        print("Error: tag is null")
        return ""
    
    return tag.split('}', 1)[-1] if '}' in tag else tag

# get_unique_addresses
#
# Purpose: Function to extract unique addresses from an MMS element
# Parameters: The MMS element to parse
# Returns: A set of unique addresses found in the MMS element
# Expects: mms_element is a valid ElementTree element with "addrs" child
#
def get_unique_addresses(mms_element):

    #get the addrs attribute
    addrs = mms_element.find("addrs")

    #set to collect unique addresses
    unique_addresses = set()

    #get all addresses from the addrs element and add them to the set
    if addrs is not None:
        for addr in addrs.findall("addr"):
            address = addr.attrib.get("address")
            if address:
                unique_addresses.add(address)
    
    return unique_addresses

# extract_body_from_mms
#
# Purpose: Function to extract the text elem body from an MMS message
# Parameters: The MMS element to parse
# Returns: The text body as a string, or an empty string if not found
# Expects: mms_element is a valid ElementTree element with "parts" child
#
def extract_body_from_mms(mms_element):
    
    # Get all the parts attributes from the message
    for parts in mms_element.findall("parts"):
        # only look at the parts with the text/plain type for the body
        for part in parts.findall("part"):
            if part.attrib.get("ct") == "text/plain":
                return part.attrib.get("text", "")
    return ""

# convert_mms_to_sms
#
# Purpose: Function to convert an MMS element to an SMS element so that all SMS
#          required tags and attributes are present by using MMS attributes
# Parameters: The MMS element to convert
# Returns: An SMS element with the required attributes filled in
# Expects: mms_element is a valid ElementTree element with "address", "date", 
#          "read", etc.
#
def convert_mms_to_sms(mms_element):
    address = mms_element.attrib.get("address", "unknown")
    date = mms_element.attrib.get("date", "0")
    read = mms_element.attrib.get("read", "1")
    sub_id = mms_element.attrib.get("sub_id", "1")
    contact_name = mms_element.attrib.get("contact_name", "")
    msg_box = mms_element.attrib.get("msg_box", "1")
    type_value = "1" if msg_box == "1" else "2"

    body = extract_body_from_mms(mms_element)

    return ET.Element("sms", {
        "protocol": "0",
        "address": address,
        "date": date,
        "type": type_value,
        "subject": "",
        "body": body,
        "toa": "null",
        "sc_toa": "null",
        "service_center": "null",
        "read": read,
        "status": "-1",
        "locked": "0",
        "date_sent": mms_element.attrib.get("date_sent", "0"),
        "sub_id": sub_id,
        "readable_date": mms_element.attrib.get("readable_date", ""),
        "contact_name": contact_name
    })

# process_messages
#
# Purpose: Function to process the messages in the XML context and convert them
#          to SMS format, filtering out group messages and invalid entries
# Parameters: The XML context iterator, new_root for SMS elements, and root for
#             handling the process iterably
# Returns: The count of valid SMS messages processed
# Expects: context is an iterable from ET.iterparse, new_root is an empty SMS 
#          root
def process_messages(context, new_root, root):
        count = 0
        for event, elem in tqdm(context):
            if event == "end" and strip_namespace(elem.tag) == "mms":

                # Skip group messages
                unique_addresses = get_unique_addresses(elem)
                if len(unique_addresses) > 2:
                    root.clear()
                    continue  

                sms = convert_mms_to_sms(elem)
                new_root.append(sms)
                count += 1
                root.clear()  # free memory

            # if message is already sms skip    
            elif event == "end" and strip_namespace(elem.tag) == "sms":
                continue

        return count

# write_output
#
# Purpose: Function to write the new XML root to an output file in pretty format
# Parameters: new_root for the SMS elements, output_file for the output path,
#            and count for the number of messages written
# Returns: None, writes the output to the specified file
# Expects: new_root is a valid ElementTree root, output_file is writable
#          and count is an integer
#
def write_output(new_root, output_file, count):
    print(f"Writing output to {output_file}...")

    # Pretty print with minidom
    xml_str = ET.tostring(new_root, encoding="utf-8")
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="    ")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"Done. Total messages written: {count}")

# Main
#
# Purpose: Main function to handle command line arguments and do all I/O
# Parameters: (FROM CL) input.xml (required), output.xml (optional)
# Returns: None, writes output to output.xml or converted.xml
# Expects: input.xml is a valid MMS XML file, output.xml is writable
#
if __name__ == "__main__":

    # Print correct usage of the script if used inccorectly
    if len(sys.argv) < 2:
        print("Usage: python convert.py <input.xml> [output.xml]")
        sys.exit(1)

    # get the I/O files
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "converted.xml"

    # Parse through the input XML file, in an iterative manner to avoid memory
    # issues
    context = ET.iterparse(input_file, events=("start", "end"))
    _, root = next(context)  # grab root
    new_root = ET.Element("smes")
    count = 0

    print("Processing...")
    count = process_messages(context, new_root, root)

    new_root.set("count", str(count))
    tree = ET.ElementTree(new_root)

    # Call the new function to write the output file
    write_output(new_root, output_file, count)
