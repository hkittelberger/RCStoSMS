import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
from tqdm import tqdm

def strip_namespace(tag):
    return tag.split('}', 1)[-1] if '}' in tag else tag

def get_unique_addresses(mms_element):
    addrs = mms_element.find("addrs")
    unique_addresses = set()
    if addrs is not None:
        for addr in addrs.findall("addr"):
            address = addr.attrib.get("address")
            if address:
                unique_addresses.add(address)
    return unique_addresses

def extract_body_from_mms(mms_element):
    """Safely extract the text body from parts of an MMS message"""
    for parts in mms_element.findall("parts"):
        for part in parts.findall("part"):
            if part.attrib.get("ct") == "text/plain":
                return part.attrib.get("text", "")
    return ""

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

# === Main Script ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert.py <input.xml> [output.xml]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "converted.xml"

    # Streaming parse
    context = ET.iterparse(input_file, events=("start", "end"))
    _, root = next(context)  # grab root
    new_root = ET.Element("smes")
    count = 0

    print("Processing...")

    for event, elem in tqdm(context):
        if event == "end" and strip_namespace(elem.tag) == "mms":
            unique_addresses = get_unique_addresses(elem)
            if len(unique_addresses) > 2:
                root.clear()
                continue  # skip group messages
            sms = convert_mms_to_sms(elem)
            new_root.append(sms)
            count += 1
            root.clear()  # free memory

        elif event == "end" and strip_namespace(elem.tag) == "sms":
            continue
            # new_root.append(elem)
            # count += 1
            # root.clear()

    new_root.set("count", str(count))
    tree = ET.ElementTree(new_root)

    print(f"Writing output to {output_file}...")

    # Pretty print with minidom
    xml_str = ET.tostring(new_root, encoding="utf-8")
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="    ")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"Done. Total messages written: {count}")
