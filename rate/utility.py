import random
import string
import re
from Crypto import Random
from Crypto.Cipher import AES
import base64
from hashlib import md5
import pandas as pd
import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom
import html
from .log import error, info

INVOKE_WEBSERVICE = True
SHOW_ADD_REMOVE_BUTTONS = True
STARTING_POSITION_OF_ACCESSORIALS = 1500
STARTING_POSITION_OF_WEIGHTBREAKS = 1800
AUTO_DELETE_UPLOADED_EXCEL_FILE = False
AUTO_DELETE_OUTPUT_CSV_FILES = False
AUTO_DELETE_OUTPUT_ZIP_FILE = False
AUTO_DELETE_OUTPUT_XML_FILE = False

def generate_key(length):
    key = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))
    return key

BLOCK_SIZE = 16

def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + (chr(length)*length).encode()

def unpad(data):
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

def bytes_to_key(data, salt, output=48):
    # extended from https://gist.github.com/gsakkis/4546068
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]

def encrypt(message, passphrase):
    salt = Random.new().read(8)
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(b"Salted__" + salt + aes.encrypt(pad(message)))

def decrypt(encrypted, passphrase):
    encrypted = base64.b64decode(encrypted)
    assert encrypted[0:8] == b"Salted__"
    salt = encrypted[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(encrypted[16:]))

def validate_password_stregnth(password):
    if len(password) < 8:
        return True, "Password must be at least 8 characters."
    if len(password) > 20:
        return True, "Password length must not be more than 20 characters."
    if not re.search(r"\d", password):
        return True, "Password must contain at least one digit."
    if not re.search(r"[A-Z]", password):
        return True, "Password must contain at least one uppercase character."
    if not re.search(r"[a-z]", password):
        return True, "Password must contain at least one lowercase character."
    if not re.search(r"\W", password):
        return True, "Password must contain at least one special character."

    return False, ""

def concat_addr(domain, input_df):
    column_name = "dummy"
    output_df = pd.DataFrame(columns = [column_name], index=range(len(input_df)))
    output_df[column_name] = ""
    try:
        if "Source Postal Code" in input_df.columns:
            output_df[column_name] = output_df[column_name] + "-" + input_df["Source Postal Code"]
        if "Source City" in input_df.columns:
            output_df[column_name] = output_df[column_name] + "-" + input_df["Source City"]
        if "Source Province Code" in input_df.columns:
            output_df[column_name] = output_df[column_name] + "-" + input_df["Source Province Code"]
        if "Source State" in input_df.columns:
            output_df[column_name] = output_df[column_name] + "-" + input_df["Source State"]
        if "Source Location" in input_df.columns:
            output_df[column_name] = output_df[column_name] + "-" + input_df["Source Location"].str[5:]
        if "Source Country Code" in input_df.columns:
            output_df[column_name] = output_df[column_name] + "-" + input_df["Source Country Code"]
        if "Source Region" in input_df.columns:
            output_df[column_name] = output_df[column_name] + "-" + input_df["Source Region"]
        if "Destination Postal Code" in input_df.columns:
            output_df[column_name] = output_df[column_name] + "-" + input_df["Destination Postal Code"]
        if "Destination City" in input_df.columns:
            output_df[column_name] = output_df[column_name] + "-" + input_df["Destination City"]
        if "Destination Province Code" in input_df.columns:
            output_df[column_name] = output_df[column_name] + "-" + input_df["Destination Province Code"]
        if "Destination State" in input_df.columns:
            output_df[column_name] = output_df[column_name] + "-" + input_df["Destination State"]
        if "Destination Location" in input_df.columns:
            output_df[column_name] = output_df[column_name] + "-" + input_df["Destination Location"].str[5:]
        if "Destination Country Code" in input_df.columns:
            output_df[column_name] = output_df[column_name] + "-" + input_df["Destination Country Code"]
        if "Destination Region" in input_df.columns:
            output_df[column_name] = output_df[column_name] + "-" + input_df["Destination Region"]

        output_df[column_name] = output_df[column_name].str.strip("-")
    except Exception as ex:
        raise Exception("concat_addr - " + str(ex))

    return output_df[column_name]

def concat_addr_row(domain, row):
    address = ""
    try:
        if "Source Postal Code" in row.index:
            address = address + "-" + row["Source Postal Code"]
        if "Source City" in row.index:
            address = address + "-" + row["Source City"]
        if "Source Province Code" in row.index:
            address = address + "-" + row["Source Province Code"]
        if "Source State" in row.index:
            address = address + "-" + row["Source State"]
        if "Source Location" in row.index:
            address = address + "-" + row["Source Location"][5:]
        if "Source Country Code" in row.index:
            address = address + "-" + row["Source Country Code"]
        if "Source Region" in row.index:
            address = address + "-" + row["Source Region"]
        if "Destination Postal Code" in row.index:
            address = address + "-" + row["Destination Postal Code"]
        if "Destination City" in row.index:
            address = address + "-" + row["Destination City"]
        if "Destination Province Code" in row.index:
            address = address + "-" + row["Destination Province Code"]
        if "Destination State" in row.index:
            address = address + "-" + row["Destination State"]
        if "Destination Location" in row.index:
            address = address + "-" + row["Destination Location"][5:]
        if "Destination Country Code" in row.index:
            address = address + "-" + row["Destination Country Code"]
        if "Destination Region" in row.index:
            address = address + "-" + row["Destination Region"]

        address = address.strip("-")
    except Exception as ex:
        raise Exception("concat_addr_row - " + str(ex))

    return address
    

def generate_xml_payload(csv_directory, csv_file_names, csv_commands):
    info("========In generate_xml_payload========")
    # Add the header elements of the XML
    xml_root = Element('Transmission')
    SubElement(xml_root, 'TransmissionHeader')
    body = SubElement(xml_root, 'TransmissionBody')

    try:
        # Open loop for each CSV file
        csv_file_names = csv_file_names
        for file_index, csv_file_name in enumerate(csv_file_names):
            # Get csv command
            csv_command_text = csv_commands[file_index]
            # Open each CSV file
            with open(os.path.join(csv_directory, csv_file_name), "r") as csv_file:
                # Add header elements for XML file
                glog = SubElement(body, 'GLogXMLElement')
                csv_data = SubElement(glog, "CSVDataLoad")
                exec_sql = ""
                # Get all lines from the CSV file
                lines = [(line) for line in csv_file]
                for index, line in enumerate(lines):
                    if index == 0:
                        csv_command = SubElement(csv_data, "CsvCommand")
                        csv_command.text = csv_command_text
                        csv_table = SubElement(csv_data, "CsvTableName")
                        csv_table.text = line.strip("\n")
                    elif index == 1:
                        csv_column_list = SubElement(csv_data, "CsvColumnList")
                        csv_column_list.text = line.strip("\n")
                    else:
                        csv_row = SubElement(csv_data, "CsvRow")
                        if line.startswith("EXEC SQL"):
                            csv_row.text = line.strip('\n') # Keep the line as it is
                        else:
                            csv_row.text = '"' + line.strip('\n').replace(",", '","') + '"' # Enclose all fields using double quotes

                # Now check if the file originally had the 2nd line starting with EXEC SQL
                if exec_sql != "":
                    # If yes then add CsvRow element at the 2nd position of the parent element CSVDataLoad
                    csv_row = Element("CsvRow")
                    csv_row.text = exec_sql.strip('\n')
                    csv_data.insert(3, csv_row)

        payload = ET.tostring(xml_root, encoding="unicode", method="xml")
        xml_file_name = "payload_" + re.findall("\d+", csv_file_names[0])[0] + ".xml"
        with open(os.path.join(csv_directory, xml_file_name), "w") as xml_file:
            dom = xml.dom.minidom.parseString(payload)
            xml_str = str(dom.toprettyxml(indent='\t', newl='\n')).replace("&quot;", '"')
            xml_file.write(xml_str)

        timestamp = re.findall("\d+", csv_file_names[0])[0]

        # Delete uploaded Excel file
        if AUTO_DELETE_UPLOADED_EXCEL_FILE:
            try:
                for file in os.listdir(csv_directory):
                    if file.lower().endswith(".xlsx") and timestamp in file:
                        os.remove(os.path.join(csv_directory, file))
                    if file.lower().endswith(".xls") and timestamp in file:
                        os.remove(os.path.join(csv_directory, file))
            except Exception as ex:
                error("Error while deleting uploaded Excel file - " + str(ex))

        # Delete output CSV files
        if AUTO_DELETE_OUTPUT_CSV_FILES:
            try:
                for file in os.listdir(csv_directory):
                    if file in csv_file_names:
                        os.remove(os.path.join(csv_directory, file))
            except Exception as ex:
                error("Error while deleting output CSV files - " + str(ex))

        # Delete output zip file
        if AUTO_DELETE_OUTPUT_ZIP_FILE:
            try:
                for file in os.listdir(csv_directory):
                    if file.lower().endswith(".zip") and timestamp in file:
                        os.remove(os.path.join(csv_directory, file))
            except Exception as ex:
                error("Error while deleting output zip file - " + str(ex))

        return "SUCCESS", "", payload
    except Exception as ex:
        error("Error while generating xml payload " + str(ex))
        return "ERROR", "Error while generating xml payload " + str(ex), ""
            
def derive_rate_offering_gid(row, domain, contract_exists, ymd, region):
    if contract_exists:
        if row["Contract Name"] not in ["<NA>", ""]:
            return domain + "." + row["Contract Name"]  
		
    if row["Offering Type"] in ["FCL", "AIR"]:
        return domain + "." + row["SCAC"] + ("-" + region if region != "" else "") + "-" + row["Offering Type"] + "-" + row["Equipment"] + "-" + row["Currency"] + "-RO-" + ymd
    else:
        return domain + "." + row["SCAC"] + ("-" + region if region != "" else "") + "-" + row["Offering Type"] + "-" + row["Currency"] + "-RO-" + ymd

def auto_complete_xml(xml_string):
    xmlstring = xml_string.replace("%%LF%%", "")
    # Convert html encoding to string
    xmlstring = html.unescape(xmlstring)
    # If a closing tag is incomplete then remove it 
    close_starts = xmlstring.rfind("</")
    close_ends = xmlstring.rfind(">")
    if close_starts > close_ends:
        # Closing tag is incomplete
        xmlstring = xmlstring[0:close_starts]

    # If a starting tag is incomplete then remove it
    open_starts = xmlstring.rfind("<")
    open_ends = xmlstring.rfind(">")
    if open_starts > open_ends:
        # Opening tag is incomplete
        xmlstring = xmlstring[0:open_starts]

    # Find all tags using regular expressions
    tag_regex = re.compile(r'<[^>]*>', re.DOTALL)
    tags = tag_regex.finditer(xmlstring)
    stack = []
    for tag in tags:
        # Get tag name
        tag_name = tag.group()
        # If the tag is self-closing then ignore
        if tag_name.endswith("/>"):
            continue
        # If the tag has attributes then remove them
        tag_name = tag_name.split(" ")[0]
        tag_name = tag_name.strip().strip(">") + ">"
        # Check if the tag is opening tag or closing tag
        if "/" not in tag_name:
            # Push to the stack if the tag is a opening tag
            stack.append(tag_name)
        else:
            # If the tag is closing tag then find the corresponding opening tag from the end of the stack
            tag_name = tag_name.replace("/", "")
            try:
                last_index_of_start_tag = len(stack) - 1 - stack[::-1].index(tag_name)
                # If the corresponding opening tag was found then pop it
                stack.pop(last_index_of_start_tag)
            except:
                pass

    # Reverse the stack and append the elements as closing tag
    stack.reverse()
    for tag in stack:
        xmlstring += tag.replace("<", "</") + "\n"

    return xmlstring


