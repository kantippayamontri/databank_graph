from graph_constants import Device, Service, HomeTree, CompanyTree, VisualNodeType
from icecream import ic


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
        for index, _service in enumerate(services):
            ic(_service.model_dump())
        
        # Create company node
        company_tree = CompanyTree(company_id="c_0", company_label="Company",
                                   services=services)
        
        return company_tree

    return None

def create_relation_service_device(home: HomeTree | None = None, company: CompanyTree | None = None):

    if (home is None) or (company is None):
        return []

    # check service that have relation with device
    service_id_list = list(_service.id for _service in company.services if _service.cate is not None)
    device_id_list= list(_device.id for _device in home.devices)

    service_device_relation = []

    for _service_id in service_id_list:
        _service = list( _service for _service in company.services if _service.id == _service_id)[0]
        for _device_id in _service.cate.keys():
            ic(_device_id, _service.cate[_device_id])
            # find device_id is exist
            if _device_id not in device_id_list:
                continue
                
            # find the leaf node of device and service
            # find service node
            service_node = company.find_node(id="c_0_s_" + _service_id)
            service_leaf = company.find_leaf(node=service_node)

            # find device node
            device_node = home.find_node(id="h_0_d_" + _device_id)
            device_leaf = home.find_leaf(node=device_node)

            service_device_relation.append(company.create_relation_visual(source=service_leaf[0].id, target=device_leaf[0].id, cls=VisualNodeType.RELATION))



    return service_device_relation