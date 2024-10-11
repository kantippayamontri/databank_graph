from graph_constants import Device, Service, HomeTree, CompanyTree
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
        ic(f"--- Devices found ---")
        # Create Home Tree
        home_tree = HomeTree(home_id="h_0", home_label="Home", devices=devices)
    
        return home_tree  
    
    return None

def create_company_tree(services: list[Service] | None):
    if len(services):
        ic(f"--- Services found ---")
        ...
        for index, _service in enumerate(services):
            ic(_service.model_dump())
        
        # Create company node
        company_tree = CompanyTree(company_id="c_0", company_label="Company",
                                   services=services)
        
        return company_tree

    return None