from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

creds = DefaultAzureCredential()

subscription_id = "4b5976c6-cdaf-4c73-9c35-78c1086a6502"

compute_client = ComputeManagementClient(creds, subscription_id)

for vm in compute_client.virtual_machines.list("myrg"):
    # print(f"VM Name: {vm.name}, VM ID: {vm.id}. VM Location: {vm.location}")
    if vm.tags['env'] == 'dev':
        print(f"Stopping VM: {vm.name} in location {vm.location}")
        compute_client.virtual_machines.begin_deallocate("myrg", vm.name).result()
    # if vm.location == "eastus":
    #     compute_client.virtual_machines.begin_deallocate("myrg", vm.name).result()
    


# for vm in compute_client.virtual_machines.list("myrg"):
#     # compute_client.virtual_machines.begin_deallocate("myrg", vm.name)
#     print(vm)

# for vm in compute_client.virtual_machines.list("myrg"):
#     print(vm.status)  

# for vm in compute_client.virtual_machines.list("myrg"):
#     vm_detail = compute_client.virtual_machines.get("myrg", vm.name, expand='instanceView')
#     for status in vm_detail.instance_view.statuses:
#         print(status)
        # if status.code.startswith('PowerState/'):
        #     print(f"Power state: {status.display_status}")