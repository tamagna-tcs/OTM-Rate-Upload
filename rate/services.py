import requests
from requests.auth import HTTPBasicAuth 
import json
import os
from datetime import datetime
from time import gmtime, strftime, mktime
import uuid
import xml.etree.ElementTree as ET
from django.conf import settings
import urllib3
from http.client import responses
import xml.dom.minidom
import html
from . import utility
from .log import error, info

def get_service_providers(instance, domain):
    info("========In get_service_providers========")
    service_providers_details = {}
    service_providers = []

    if utility.INVOKE_WEBSERVICE:
        try:
            dt = datetime.fromtimestamp(mktime(gmtime())) # Get current date in UTC
            current_date = dt.isoformat() # Change the format
            url = instance.otm_url.rstrip("/") +  ":443/GC3Services/CommandService/call"
            headers = {'content-type': 'text/xml'}
            body = f'''<soapenv:Envelope xmlns:com="http://xmlns.oracle.com/apps/otm/CommandService" xmlns:dbx="http://xmlns.oracle.com/apps/otm/DBXML" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Header>
                    <wsse:Security soapenv:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                        <wsse:UsernameToken wsu:Id="UsernameToken-{str(uuid.uuid4().hex).upper()}">
                            <wsse:Username>{instance.otm_user}</wsse:Username>
                            <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{instance.otm_password}</wsse:Password>
                            <wsu:Created>{current_date}</wsu:Created>
                        </wsse:UsernameToken>
                    </wsse:Security>
                </soapenv:Header>
                <soapenv:Body>
                    <com:xmlExport>
                        <dbx:sql2xml>
                            <dbx:Query>
                            <dbx:RootName>SERVICE_PROV</dbx:RootName>
                            <dbx:Statement>SELECT SERV.SERVPROV_XID, LOC.LOCATION_NAME, SERV.SCAC_GID FROM SERVPROV SERV, LOCATION LOC WHERE 1=1 AND SERV.SERVPROV_GID = LOC.LOCATION_GID AND SERV.DOMAIN_NAME NOT IN ('PUBLIC')</dbx:Statement>
                            </dbx:Query>
                        </dbx:sql2xml>
                    </com:xmlExport>
                </soapenv:Body>
                </soapenv:Envelope>'''

            response = requests.post(url, data=body, headers=headers, auth=HTTPBasicAuth(instance.otm_user, instance.otm_password))
            info("Status code " + str(response.status_code))
            if response.status_code != 200:
                error(f"get_service_providers - response code {response.status_code} - {str(response)}")
            root = ET.fromstring(str(response.text))
            for record in root.iter("SERVICE_PROV"):
                service_providers.append(str(record.get("LOCATION_NAME")))
                provider_name = ""
                scac = ""
                provider_id = str(record.get("SERVPROV_XID", ""))
                provider_name = str(record.get("LOCATION_NAME", ""))
                scac = str(record.get("SCAC_GID", "")).replace(domain+".", "")
                service_providers_details[provider_name] = {"id" : provider_id, "scac" : scac}
        
            info("Count of Service Providers " + str(len(service_providers)))
            return service_providers, service_providers_details

        except Exception as e:
            error("get_service_providers - " + str(e))
            return [], {}
    else:
        try:
            tree = ET.parse(os.path.join(settings.MEDIA_ROOT, "service_providers.xml"))
            root = tree.getroot()
            for record in root.iter("SERVICE_PROV"):
                service_providers.append(str(record.get("LOCATION_NAME")))
                provider_name = ""
                scac = ""
                provider_id = str(record.get("SERVPROV_XID", ""))
                provider_name = str(record.get("LOCATION_NAME", ""))
                scac = str(record.get("SCAC_GID", "")).replace(domain+".", "")
                service_providers_details[provider_name] = {"id" : provider_id, "scac" : scac}

            info("Count of Service Providers " + str(len(service_providers)))        
            return service_providers, service_providers_details

        except Exception as e:
            error("get_service_providers - " + str(e))
            return [], {}

def get_instance_status(instance):
    info("========In get_instance_status========")
    info("Instance name " + instance.instance_name)
    if not utility.INVOKE_WEBSERVICE:
        return "DOWN"

    rest_url = instance.otm_url.rstrip("/") + "/logisticsRestApi/resources-int/v2/serviceProviders"
    params = {"fields":"servprovXid", "limit": 1}
    try:
        response = requests.get(rest_url, params=params, auth=HTTPBasicAuth(instance.otm_user, instance.otm_password))
        info("Status code " + str(response.status_code))
        if response.status_code != 200:
            error(f"get_instance_status - response code {response.status_code} - {str(response)}")
    except:
        return "DOWN"

    if response.ok:
        return "UP"
    else:
        return "DOWN"

def get_equipments(instance):
    info("========In get_equipments========")
    rest_url = instance.otm_url.rstrip("/") + "/logisticsRestApi/resources-int/v2/equipmentGroups"
    params = {"q":"domainName ne \"PUBLIC\"", "limit": 100, "fields":"equipmentGroupXid"}
    try:
        equipments = []
        if utility.INVOKE_WEBSERVICE:
            response = requests.get(rest_url, params=params, auth=HTTPBasicAuth(instance.otm_user, instance.otm_password))
            info("Status code " + str(response.status_code))
            if response.status_code != 200:
                error(f"get_equipments - response code {response.status_code} - {str(response)}")
            payload = response.json()
            equipments = [(item["equipmentGroupXid"]) for item in payload["items"] if "equipmentGroupXid" in item]
        else:
            json_data = open(os.path.join(settings.MEDIA_ROOT, "equipments.json"))   
            payload = json.load(json_data)
            equipments = [(item["equipmentGroupXid"]) for item in payload["items"] if "equipmentGroupXid" in item]

        info("Count of Equipments " + str(len(equipments)))
        return equipments
    except Exception as e:
        error("get_equipments - " + str(e))
        return []

def get_contracts(instance, service_provider, domain_name, mode):
    info("========In get_contracts========")
    info("Service provider " + service_provider)
    contracts = []
    if utility.INVOKE_WEBSERVICE:
        dt = datetime.fromtimestamp(mktime(gmtime())) # Get current date in UTC
        current_date = dt.isoformat() # Change the format
        url = instance.otm_url.rstrip("/") +  ":443/GC3Services/CommandService/call"
        headers = {'content-type': 'text/xml'}
        body = f'''<soapenv:Envelope xmlns:com="http://xmlns.oracle.com/apps/otm/CommandService" xmlns:dbx="http://xmlns.oracle.com/apps/otm/DBXML" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Header>
                <wsse:Security soapenv:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    <wsse:UsernameToken wsu:Id="UsernameToken-{str(uuid.uuid4().hex).upper()}">
                        <wsse:Username>{instance.otm_user}</wsse:Username>
                        <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{instance.otm_password}</wsse:Password>
                        <wsu:Created>{current_date}</wsu:Created>
                    </wsse:UsernameToken>
                </wsse:Security>
            </soapenv:Header>
            <soapenv:Body>
                <com:xmlExport>
                    <dbx:sql2xml>
                        <dbx:Query>
                        <dbx:RootName>OBLINE</dbx:RootName>
                        <dbx:Statement>select ro.RATE_OFFERING_XID from rate_offering ro, servprov sp, location loc where ro.SERVPROV_GID = sp.SERVPROV_GID and loc.location_gid = sp.SERVPROV_GID and loc.location_name = '{service_provider}' and ro.IS_ACTIVE = 'Y' and ro.RATE_OFFERING_TYPE_GID not in ('LTL-SMC')</dbx:Statement>
                        </dbx:Query>
                    </dbx:sql2xml>
                </com:xmlExport>
            </soapenv:Body>
            </soapenv:Envelope>'''

        try:
            response = requests.post(url, data=body, headers=headers, auth=HTTPBasicAuth(instance.otm_user, instance.otm_password))
            info("Status code " + str(response.status_code))
            if response.status_code != 200:
                error(f"get_contracts - response code {response.status_code} - {str(response)}")
            root = ET.fromstring(str(response.text))
            for record in root.iter("OBLINE"):
                contracts.append(str(record.get("RATE_OFFERING_XID")))

            info("Count of Contracts " + str(len(contracts)))
            return contracts
        except Exception as e:
            error("get_contracts - " + str(e))
            return []
    else:
        try:
            tree = ET.parse(os.path.join(settings.MEDIA_ROOT, "contracts.xml"))
            root = tree.getroot()
            for record in root.iter("OBLINE"):
                contracts.append(str(record.get("RATE_OFFERING_XID")))

            info("Count of Contracts " + str(len(contracts)))
            return contracts
        except Exception as e:
            error("get_contracts - " + str(e))
            return []

def get_acessorial_codes(instance):
    info("========In get_acessorial_codes========")
    rest_url = instance.otm_url.rstrip("/") + "/logisticsRestApi/resources-int/v2/accessorialCodes"
    params = {"q":"domainName ne \"PUBLIC\"", "limit": 100, "fields":"accessorialCodeXid"}
    try:
        costs = []
        if utility.INVOKE_WEBSERVICE:
            response = requests.get(rest_url, params=params, auth=HTTPBasicAuth(instance.otm_user, instance.otm_password))
            info("Status code " + str(response.status_code))
            if response.status_code != 200:
                error(f"get_acessorial_codes - response code {response.status_code} - {str(response)}")
            payload = response.json()
            costs = [(item["accessorialCodeXid"]) for item in payload["items"] if "accessorialCodeXid" in item]
        else:
            json_data = open(os.path.join(settings.MEDIA_ROOT, "accessorial_codes.json"))   
            payload = json.load(json_data)
            costs = [(item["accessorialCodeXid"]) for item in payload["items"] if "accessorialCodeXid" in item]

        info("Count of Acessorial Codes " + str(len(costs)))
        return costs
    except Exception as e:
        error("get_acessorial_codes - " + str(e))
        return []

def get_regions(instance):
    info("========In get_regions========")
    rest_url = instance.otm_url.rstrip("/") + "/logisticsRestApi/resources-int/v2/regions"
    params = {"q":"domainName ne \"PUBLIC\"", "limit": 100, "fields":"regionXid"}
    try:
        costs = []
        if utility.INVOKE_WEBSERVICE:
            response = requests.get(rest_url, params=params, auth=HTTPBasicAuth(instance.otm_user, instance.otm_password))
            info("Status code " + str(response.status_code))
            if response.status_code != 200:
                error(f"get_regions - response code {response.status_code} - {str(response)}")
            payload = response.json()
            costs = [(item["regionXid"]) for item in payload["items"] if "regionXid" in item]
        else:
            json_data = open(os.path.join(settings.MEDIA_ROOT, "regions.json"))   
            payload = json.load(json_data)
            costs = [(item["regionXid"]) for item in payload["items"] if "regionXid" in item]

        info("Count of Regions " + str(len(costs)))
        return costs
    except Exception as e:
        error("get_regions - " + str(e))
        return []

def get_unit_break_profiles(instance, uom_type):
    info("========In get_unit_break_profiles========")
    info("UOM type " + uom_type)
    rest_url = instance.otm_url.rstrip("/") + "/logisticsRestApi/resources-int/v2/rateUnitBreakProfiles"
    params = {"q":"domainName ne \"PUBLIC\" and uomType eq \"" + uom_type + "\"", "limit": 100, "fields":"rateUnitBreakProfileXid"}
    try:
        profiles = []
        if utility.INVOKE_WEBSERVICE:
            response = requests.get(rest_url, params=params, auth=HTTPBasicAuth(instance.otm_user, instance.otm_password))
            info("Status code " + str(response.status_code))
            if response.status_code != 200:
                error(f"get_unit_break_profiles - response code {response.status_code} - {str(response)}")
            payload = response.json()
            profiles = [(item["rateUnitBreakProfileXid"]) for item in payload["items"] if "rateUnitBreakProfileXid" in item]
        else:
            json_data = open(os.path.join(settings.MEDIA_ROOT, "unit_break_profile.json"))   
            payload = json.load(json_data)
            profiles = [(item["rateUnitBreakProfileXid"]) for item in payload["items"] if "rateUnitBreakProfileXid" in item]

        info("Count of Unit Break Profiles " + str(len(profiles)))
        return profiles
    except Exception as e:
        error("get_unit_break_profiles " + str(e))
        return []

def get_weight_break(instance, break_profile):
    info("========In get_weight_break========")
    info("Break profile " + break_profile)
    weight_breaks = []
    if utility.INVOKE_WEBSERVICE:
        try:
            dt = datetime.fromtimestamp(mktime(gmtime())) # Get current date in UTC
            current_date = dt.isoformat() # Change the format
            url = instance.otm_url.rstrip("/") +  ":443/GC3Services/CommandService/call"
            headers = {'content-type': 'text/xml'}
            body = f'''<soapenv:Envelope xmlns:com="http://xmlns.oracle.com/apps/otm/CommandService" xmlns:dbx="http://xmlns.oracle.com/apps/otm/DBXML" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Header>
                    <wsse:Security soapenv:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                        <wsse:UsernameToken wsu:Id="UsernameToken-{str(uuid.uuid4().hex).upper()}">
                            <wsse:Username>{instance.otm_user}</wsse:Username>
                            <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{instance.otm_password}</wsse:Password>
                            <wsu:Created>{current_date}</wsu:Created>
                        </wsse:UsernameToken>
                    </wsse:Security>
                </soapenv:Header>
                <soapenv:Body>
                    <com:xmlExport>
                        <dbx:sql2xml>
                            <dbx:Query>
                            <dbx:RootName>RATE_UNIT_BREAK</dbx:RootName>
                            <dbx:Statement>SELECT RUB.RATE_UNIT_BREAK_GID, RUB.RATE_UNIT_BREAK_XID || ' - ' || SUBSTR(RUB.RATE_UNIT_BREAK_MAX, 1, (INSTR(RUB.RATE_UNIT_BREAK_MAX, ' '))-1) WEIGHT_BREAK FROM RATE_UNIT_BREAK RUB, RATE_UNIT_BREAK_PROFILE RUBP WHERE 1 = 1 AND RUB.RATE_UNIT_BREAK_PROFILE_GID = RUBP.RATE_UNIT_BREAK_PROFILE_GID AND RUBP.RATE_UNIT_BREAK_PROFILE_XID = '{break_profile}' ORDER BY TO_NUMBER(RUB.RATE_UNIT_BREAK_XID)</dbx:Statement>
                            </dbx:Query>
                        </dbx:sql2xml>
                    </com:xmlExport>
                </soapenv:Body>
                </soapenv:Envelope>'''

            response = requests.post(url, data=body, headers=headers, auth=HTTPBasicAuth(instance.otm_user, instance.otm_password))
            info("Status code " + str(response.status_code))
            if response.status_code != 200:
                error(f"get_weight_break - response code {response.status_code} - {str(response)}")
            root = ET.fromstring(str(response.text))
            for record in root.iter("RATE_UNIT_BREAK"):
                weight_break = str(record.get("WEIGHT_BREAK", ""))
                weightBreakGid = str(record.get("RATE_UNIT_BREAK_GID", ""))
                if weight_break != "": 
                    weight_breaks.append({"WeightBreak" : weight_break, "WeightBreakGid" : weightBreakGid})
                
            info("Count of weight_breaks " + str(len(weight_breaks)))        
            return weight_breaks

        except Exception as e:
            error("get_weight_break - " + str(e))
            return []

    else:
        try:
            tree = ET.parse(os.path.join(settings.MEDIA_ROOT, "weight_break.xml"))
            root = tree.getroot()
            for record in root.iter("RATE_UNIT_BREAK"):
                weight_break = str(record.get("WEIGHT_BREAK", ""))
                weightBreakGid = str(record.get("RATE_UNIT_BREAK_GID", ""))
                if weight_break != "": 
                    weight_breaks.append({"WeightBreak" : weight_break, "WeightBreakGid" : weightBreakGid})
            
            info("Count of weight_breaks " + str(len(weight_breaks)))        
            return weight_breaks
        except Exception as e:
            error("get_weight_break - " + str(e))
            return []                                                                               
    

def push_rate_to_otm(instance, payload):
    info("========In push_rate_to_otm========")

    if utility.INVOKE_WEBSERVICE:
        try:
            url = instance.otm_url.rstrip("/") +  "/GC3/glog.integration.servlet.WMServlet"
            http = urllib3.PoolManager()
            headers = urllib3.make_headers(basic_auth='{}:{}'.format(instance.otm_user, instance.otm_password))
            # Invoke request
            response = http.request('POST', url, headers=headers, body=payload)
            # Get http status
            http_status = response.status
            http_status_code = responses[http_status]
            info("Status " + str(http_status))
            # If status is not 200 then return error
            if http_status != 200:
                error(f"push_rate_to_otm - response code {str(http_status)} - {response.data}")
                return "ERROR", http_status_code, ""

            response_data = response.data.decode("utf-8").strip("\n")
            root = ET.fromstring(response_data)
            transmission_no = ""
            for record in root.iter("ReferenceTransmissionNo"):
                transmission_no = str(record.text)
            # If Transmission No is -1 then return error
            if transmission_no == "" or transmission_no == "-1":
                error_message = ""
                for record in root.iter("StackTrace"):
                    error_message = str(record.text)

                error("Error was retutned by OTM - " + error_message)
                return "ERROR", error_message, ""

            return "SUCCESS", "Rate files have been uploaded to OTM.", transmission_no

        except Exception as ex:
            error("Error while uploading rates to OTM - " + str(ex))
            return "ERROR", "Error while uploading rates to OTM - " + str(ex), ""
    else:
        return "ERROR", "This feature has been disabled, please contact ADMIN.", ""
    

def get_transmission_status(instance, transmission_no):
    info("========In get_transmission_status========")
    info("transmission_no " + str(transmission_no))
    error_details = []
    # query = f"select to_char(substr(IL.I_MESSAGE_TEXT, 1, 4000)) STATUS from I_TRANSMISSION ITR,I_LOG IL where IL.I_TRANSMISSION_NO = ITR.I_TRANSMISSION_NO and ITR.I_TRANSMISSION_NO = '{str(transmission_no)}' and ((IL.I_MESSAGE_CLASS = 'I' and IL.I_MESSAGE_CODE = 'CSV_PROCESSING_RESULTS' and I_MESSAGE_TEXT like '%ORA%') or (IL.I_MESSAGE_CLASS = 'E'))"
    query = f"select to_char(substr(IL.I_MESSAGE_TEXT, 1, 4000)) STATUS from I_TRANSMISSION ITR,I_LOG IL where IL.I_TRANSMISSION_NO = ITR.I_TRANSMISSION_NO and ITR.I_TRANSMISSION_NO = '{str(transmission_no)}'"
    try:
        dt = datetime.fromtimestamp(mktime(gmtime())) # Get current date in UTC
        current_date = dt.isoformat() # Change the format
        url = instance.otm_url.rstrip("/") +  ":443/GC3Services/CommandService/call"
        headers = {'content-type': 'text/xml'}
        body = f'''<soapenv:Envelope xmlns:com="http://xmlns.oracle.com/apps/otm/CommandService" xmlns:dbx="http://xmlns.oracle.com/apps/otm/DBXML" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Header>
                <wsse:Security soapenv:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                    <wsse:UsernameToken wsu:Id="UsernameToken-{str(uuid.uuid4().hex).upper()}">
                        <wsse:Username>{instance.otm_user}</wsse:Username>
                        <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{instance.otm_password}</wsse:Password>
                        <wsu:Created>{current_date}</wsu:Created>
                    </wsse:UsernameToken>
                </wsse:Security>
            </soapenv:Header>
            <soapenv:Body>
                <com:xmlExport>
                    <dbx:sql2xml>
                        <dbx:Query>
                        <dbx:RootName>Order</dbx:RootName>
                        <dbx:Statement>{query}</dbx:Statement>
                        </dbx:Query>
                    </dbx:sql2xml>
                </com:xmlExport>
            </soapenv:Body>
            </soapenv:Envelope>'''

        response = requests.post(url, data=body, headers=headers, auth=HTTPBasicAuth(instance.otm_user, instance.otm_password))
        info("Status code " + str(response.status_code))
        if response.status_code != 200:
            error(f"get_transmission_status - response code {response.status_code} - {str(response)}")

        #info(response.text)

        if 'NO DATA' in str(response.text):
            print("NO DATA found in response.text")
            print(str(response.text))
            if not is_transmission_completed(response.text):
                return "PROCESSING", ""
            
        outcome = "SUCCESS"

        nsmap = {"ns0": "http://schemas.xmlsoap.org/soap/envelope/", "ns1": "http://xmlns.oracle.com/apps/otm/CommandService", "ns2": "http://xmlns.oracle.com/apps/otm/DBXML"}
        tree = ET.ElementTree(ET.fromstring(response.text))
        xroot = tree.getroot()

        print("Conversion done")
        for node in xroot.findall("ns0:Body/ns1:xmlExportResponse/ns2:xml2sql/ns2:TRANSACTION_SET/Order", nsmap):
            status_node = node.attrib.get("STATUS", "").replace("%%LF%%", "")
            if not status_node:
                continue

            status_node = utility.auto_complete_xml(status_node)
            print(xml.dom.minidom.parseString(status_node).toprettyxml().replace("&quot;", '"'))

            table_name = "Unknown"
            processed = ""
            errored = ""
            skipped = ""
            exceptions = []

            try:
                tree_node = ET.ElementTree(ET.fromstring(status_node))
                xroot_node = tree_node.getroot()
                print("Conversion done in loop")

                # Get table name and counts
                try:
                    table_name = xroot_node.findall(".//TableName")[0].text
                    processed = xroot_node.findall(".//ProcessCount")[0].text
                    errored = xroot_node.findall(".//ErrorCount")[0].text
                    skipped = xroot_node.findall(".//SkipCount")[0].text

                    if (errored and int(errored) > 0) or len(xroot_node.findall(".//Error")) > 0:
                        outcome = "ERROR"

                    for child_node in xroot_node.findall(".//Error"):
                        exception_node = child_node.find("Exception")
                        data_node = child_node.find("Data")
                        if exception_node is not None and data_node is not None:
                            exceptions.append("Error: " + str(exception_node.text) + "\nData: " + str(data_node.text))

                except Exception as ex:
                    print("Error while parsing XML " + str(ex))
                    print(status_node)
                    exceptions.append("Error is more than 4000 characters, check the error in OTM.")                

            except Exception as ex:
                print("Error while parsing XML " + str(ex))
                print(status_node)
                exceptions.append("Error string is more than 4000 characters, check the error in OTM.")

            error_details.append({
                "table_name" : table_name,
                "processed" : processed,
                "errored" : errored,
                "skipped" : skipped,
                "exceptions" : exceptions
            })

        print(error_details)

        return outcome, error_details

    except Exception as e:
        error("get_transmission_status - " + str(e))
        return "ERROR", [{
                "table_name" : "unknown",
                "processed" : "",
                "errored" : "",
                "skipped" : "",
                "exceptions" : ["Error while retrieving transmission status"]
            }]


def is_transmission_completed(response):
    info("========In is_transmission_successfully_completed========")
    try:
        # info(html.unescape(response.replace("%%LF%%", "")))

        if 'NO DATA' in str(response):
            return False # No data was retutned by SQL, which means data is still being processed

        nsmap = {"ns0": "http://schemas.xmlsoap.org/soap/envelope/", "ns1": "http://xmlns.oracle.com/apps/otm/CommandService", "ns2": "http://xmlns.oracle.com/apps/otm/DBXML"}
        tree = ET.ElementTree(ET.fromstring(response))
        print("Converted whole string into xml")
        xroot = tree.getroot()

        for node in xroot.findall("ns0:Body/ns1:xmlExportResponse/ns2:xml2sql/ns2:TRANSACTION_SET/Order", nsmap):
            status_node = node.attrib.get("STATUS", "").replace("%%LF%%", "")
            # status_node = html.unescape(status_node)
            if status_node != "":                
                print("xml row - ")
                # print(status_node)
                try:
                    tree_node = ET.ElementTree(ET.fromstring(status_node))
                    print("Converted it into xml")
                    xroot_node = tree_node.getroot()

                    if len(xroot_node.findall(".//ElapsedTime")) == 0:
                        return False # ElapnsedTime not found in XML, so it's still processing
                    
                except Exception as ex:
                    error("is_transmission_completed while pasring xml " + str(ex))

        return True

    except Exception as e:
        error("is_transmission_completed - " + str(e))
        return False
    

def max_cost_seq(instance):
    info("========In max_cost_seq========")
    if utility.INVOKE_WEBSERVICE:
        try:
            dt = datetime.fromtimestamp(mktime(gmtime())) # Get current date in UTC
            current_date = dt.isoformat() # Change the format
            url = instance.otm_url.rstrip("/") +  ":443/GC3Services/CommandService/call"
            headers = {'content-type': 'text/xml'}
            body = f'''<soapenv:Envelope xmlns:com="http://xmlns.oracle.com/apps/otm/CommandService" xmlns:dbx="http://xmlns.oracle.com/apps/otm/DBXML" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Header>
                    <wsse:Security soapenv:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                        <wsse:UsernameToken wsu:Id="UsernameToken-{str(uuid.uuid4().hex).upper()}">
                            <wsse:Username>{instance.otm_user}</wsse:Username>
                            <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{instance.otm_password}</wsse:Password>
                            <wsu:Created>{current_date}</wsu:Created>
                        </wsse:UsernameToken>
                    </wsse:Security>
                </soapenv:Header>
                <soapenv:Body>
                    <com:xmlExport>
                        <dbx:sql2xml>
                            <dbx:Query>
                            <dbx:RootName>MAX_SEQ</dbx:RootName>
                            <dbx:Statement>SELECT MAX(RATE_GEO_COST_SEQ) MAX_VALUE FROM RATE_GEO_COST</dbx:Statement>
                            </dbx:Query>
                        </dbx:sql2xml>
                    </com:xmlExport>
                </soapenv:Body>
                </soapenv:Envelope>'''

            response = requests.post(url, data=body, headers=headers, auth=HTTPBasicAuth(instance.otm_user, instance.otm_password))
            info("Status code " + str(response.status_code))
            if response.status_code != 200:
                error(f"max_cost_group_seq - response code {response.status_code} - {str(response)}")
            root = ET.fromstring(str(response.text))
            max_value = "0"
            for record in root.iter("MAX_SEQ"):
                max_value = str(record.get("MAX_VALUE"))
                
            info("Max cost sequence value " + max_value)
            return int(max_value) + 1

        except Exception as e:
            error("max_cost_seq - " + str(e))
            return 0
    else:
        return 0
    
def max_cost_group_seq(instance):
    info("========In max_cost_group_seq========")
    if utility.INVOKE_WEBSERVICE:
        try:
            dt = datetime.fromtimestamp(mktime(gmtime())) # Get current date in UTC
            current_date = dt.isoformat() # Change the format
            url = instance.otm_url.rstrip("/") +  ":443/GC3Services/CommandService/call"
            headers = {'content-type': 'text/xml'}
            body = f'''<soapenv:Envelope xmlns:com="http://xmlns.oracle.com/apps/otm/CommandService" xmlns:dbx="http://xmlns.oracle.com/apps/otm/DBXML" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                <soapenv:Header>
                    <wsse:Security soapenv:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                        <wsse:UsernameToken wsu:Id="UsernameToken-{str(uuid.uuid4().hex).upper()}">
                            <wsse:Username>{instance.otm_user}</wsse:Username>
                            <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{instance.otm_password}</wsse:Password>
                            <wsu:Created>{current_date}</wsu:Created>
                        </wsse:UsernameToken>
                    </wsse:Security>
                </soapenv:Header>
                <soapenv:Body>
                    <com:xmlExport>
                        <dbx:sql2xml>
                            <dbx:Query>
                            <dbx:RootName>MAX_SEQ</dbx:RootName>
                            <dbx:Statement>SELECT MAX(RATE_GEO_COST_GROUP_SEQ) MAX_VALUE FROM RATE_GEO_COST_GROUP</dbx:Statement>
                            </dbx:Query>
                        </dbx:sql2xml>
                    </com:xmlExport>
                </soapenv:Body>
                </soapenv:Envelope>'''

            response = requests.post(url, data=body, headers=headers, auth=HTTPBasicAuth(instance.otm_user, instance.otm_password))
            info("Status code " + str(response.status_code))
            if response.status_code != 200:
                error(f"max_cost_group_seq - response code {response.status_code} - {str(response)}")
            root = ET.fromstring(str(response.text))
            max_value = "0"
            for record in root.iter("MAX_SEQ"):
                max_value = str(record.get("MAX_VALUE"))
                
            info("Max cost sequence value " + max_value)
            return int(max_value) + 1

        except Exception as e:
            error("max_cost_group_seq - " + str(e))
            return 0
    else:
        return 0