from graph_constants import Device, Service, HomeTree, CompanyTree, VisualNodeType
from icecream import ic
import json

device_category_mapping = {
    ("Average", "Daily", "Low"): "Private",
    ("Transfer", "Daily", "Low"): "Private",
    ("Anonymise", "Daily", "Low"): "Private",
    ("Average", "Daily", "High"): "Protected",
    ("Transfer", "Daily", "High"): "Protected",
    ("Anonymise", "Daily", "High"): "Protected",
    ("Average", "Daily", "Medium"): "Secert",
    ("Transfer", "Daily", "Medium"): "Secert",
    ("Anonymise", "Daily", "Medium"): "Secert",
    ("Average", "Weekly", "Low"): "Confidential",
    ("Transfer", "Weekly", "Low"): "Confidential",
    ("Anonymise", "Weekly", "Low"): "Confidential",
    ("Average", "Weekly", "High"): "Restricted",
    ("Transfer", "Weekly", "High"): "Restricted",
    ("Anonymise", "Weekly", "High"): "Restricted",
    ("Average", "Monthly", "Low"): "Private",
    ("Transfer", "Monthly", "Low"): "Private",
    ("Anonymise", "Monthly", "Low"): "Private",
    ("Average", "Monthly", "High"): "Protected",
    ("Transfer", "Monthly", "High"): "Protected",
    ("Anonymise", "Monthly", "High"): "Protected",
    ("Average", "Monthly", "Medium"): "Protected",
    ("Transfer", "Monthly", "Medium"): "Protected",
    ("Anonymise", "Monthly", "Medium"): "Protected",
    ("Average", "Yearly", "Low"): "Confidential",
    ("Transfer", "Yearly", "Low"): "Confidential",
    ("Anonymise", "Yearly", "Low"): "Confidential",
    ("Average", "Yearly", "High"): "Restricted",
    ("Transfer", "Yearly", "High"): "Secret",
    ("Average", "Yearly", "High"): "Restricted",
    ("Upload", "Yearly", "Medium"): "Protected",
}

service_category_mapping = {
    ("View Data", "Daily", "Low"): "Low trust",
    ("View Data", "Daily", "Medium"): "Medium trust",
    ("View Data", "Daily", "High"): "High trust",
    ("View Report", "Daily", "Low"): "Low trust",
    ("View Report", "Daily", "Medium"): "Medium trust",
    ("View Report", "Daily", "High"): "High trust",
    ("Read Data", "Daily", "Low"): "High distrust",
    ("Read Data", "Daily", "Medium"): "Low trust",
    ("Read Data", "Daily", "High"): "Medium trust",
    ("View Data", "Weekly", "Low"): "Low trust",
    ("View Data", "Weekly", "Medium"): "Medium trust",
    ("View Data", "Weekly", "High"): "High trust",
    ("View Report", "Weekly", "Low"): "High distrust",
    ("View Report", "Weekly", "Medium"): "Low trust",
    ("View Report", "Weekly", "High"): "Medium trust",
    ("Read Data", "Weekly", "Low"): "Distrust",
    ("Read Data", "Weekly", "Medium"): "High distrust",
    ("Read Data", "Weekly", "High"): "Low trust",
    ("View Data", "Monthly", "Low"): "High distrust",
    ("View Data", "Monthly", "Medium"): "Low trust",
    ("View Data", "Monthly", "High"): "Medium trust",
    ("View Report", "Monthly", "Low"): "Distrust",
    ("Report Data", "Daily", "Low"): "Medium trust",
    ("View Report", "Monthly", "Medium"): "Medium trust",
    ("View Report", "Monthly", "High"): "High trust",
    ("Read Data", "Monthly", "Low"): "Distrust",
    ("Read Data", "Monthly", "Medium"): "Distrust",
    ("Read Data", "Monthly", "High"): "Low trust",
    ("View Data", "Yearly", "Low"): "Distrust",
    ("View Data", "Yearly", "Medium"): "Medium trust",
    ("View Data", "Yearly", "High"): "High trust",
    ("View Report", "Yearly", "Low"): "Distrust",
    ("View Report", "Yearly", "Medium"): "Distrust",
    ("View Report", "Yearly", "High"): "Low trust",
    ("Read Data", "Yearly", "Low"): "Distrust",
    ("Read Data", "Yearly", "Medium"): "Distrust",
    ("Read Data", "Yearly", "High"): "Distrust",
}


# code to generate graph
def create_elements(
    _data: dict | None,
) -> tuple[list[Device] | None, list[Service] | None]:
    data: dict | None = _data
    # check device
    if not data:
        return None, None

    devices = []
    if "devices" in data.keys():
        for device_id in data["devices"].keys():
            if "raw_data" not in data["devices"][device_id].keys():
                data["devices"][device_id]["raw_data"] = None
            device = Device(**data["devices"][device_id], id=device_id)
            devices.append(device)
    else:
        ic(f"Devices not found.")

    services = []
    if "services" in data.keys():
        for service_id in data["services"].keys():
            if "cate_service" not in data["services"][service_id].keys():
                data["services"][service_id]["cate_service"] = None
            service = Service(
                **data["services"][service_id],
                id=service_id,
            )
            services.append(service)
    else:
        ic(f"Services not found.")

    return devices, services


def create_home_tree(
    devices: list[Device] | None):
    if len(devices):
        # Create Home Tree
        home_tree = HomeTree(home_id="h_0", home_label="Home", devices=devices)
    
        return home_tree  
    
    return None

def create_company_tree(services: list[Service] | None):
    if len(services):
        # for index, _service in enumerate(services):
        #     ic(_service.model_dump())
        
        # Create company node
        company_tree = CompanyTree(company_id="c_0", company_label="Company",
                                services=services)
        
        return company_tree

    return None

def create_relation_service_device(home: HomeTree | None = None, company: CompanyTree | None = None):

    if (home is None) or (company is None):
        return []

    # check service that have relation with device
    # device_id_list= list(_device.id for _device in home.devices)
    # service_id_list= []
    # service_id_list = list(_service.id for _service in company.services if _service.cate is not None)
    with open('./mock_data.json', 'r') as file:
        data = json.load(file)
    data = data["data"]
    same_length = []
    service_device_relation = []
    devices = data['devices']
    services = data['services']
    for device_id in devices:
        if 'raw_data' in devices[device_id]:
            for device_unprocessed in devices[device_id]['raw_data']:
                for service_id in services:
                    if 'cate_service' in services[service_id]:
                        for service_device_id in services[service_id]['cate_service']:
                            for data_cat in services[service_id]['cate_service'][service_device_id]:
                                # print(data_cat == device_unprocessed,device_unprocessed,data_cat)
                                if data_cat == device_unprocessed and device_id == service_device_id:
                                    # print(data_cat,device_unprocessed)
                                    service_node = company.find_node(id="c_0_s_" + service_id)
                                    service_leaf = company.find_leaf(node=service_node)
                                    device_node = home.find_node(id="h_0_d_" + device_id)
                                    device_leaf = home.find_leaf(node=device_node)
                                    for se_leaf in service_leaf:
                                        _action = services[service_id]['cate_service'][service_device_id][data_cat]["action"]
                                        _frequency = services[service_id]['cate_service'][service_device_id][data_cat]["frequency"]
                                        _category = services[service_id]['cate_service'][service_device_id][data_cat]["category"]
                                        trust_key = (_action, _frequency, _category)
                                        trust_level = (
                                            service_category_mapping[trust_key]
                                            if trust_key in service_category_mapping.keys()
                                            else "Low trust"
                                        )
                                        # if data_cat == device_unprocessed == "Device Information" and device_id == service_device_id:
                                        #         print(services[service_id]['cate_service'][service_device_id][data_cat]["action"].replace(' ','_')  +"------------------"+("st_" +trust_level).replace(' ','_') +",,,,,,,,,"+ se_leaf.id)
                                        if services[service_id]["service_type"].replace(" ","_") in se_leaf.id and services[service_id]['cate_service'][service_device_id][data_cat]["action"].replace(' ','_') in se_leaf.id and ("st_" +trust_level).replace(' ','_') in se_leaf.id:
                                            for de_leaf in device_leaf:
                                                sen_key = (
                                                    devices[device_id]["raw_data"][device_unprocessed]["action"],
                                                    devices[device_id]["raw_data"][device_unprocessed]["frequency"],
                                                    devices[device_id]["raw_data"][device_unprocessed]["sensitivity"],
                                                )
                                                sensitivity = (
                                                    device_category_mapping[sen_key]
                                                    if sen_key in device_category_mapping.keys()
                                                    else "Private"
                                                )
                                                if device_unprocessed.replace(' ','_') in de_leaf.id and devices[device_id]['raw_data'][device_unprocessed]['action'].replace(' ','_') in de_leaf.id and ("sen_" +sensitivity).replace(' ','_') in de_leaf.id:
                                                    service_device_relation.append(company.create_relation_visual(source=se_leaf.id, target=de_leaf.id, cls=VisualNodeType.RELATION_BETWEEN))
    
    return service_device_relation