from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

cerdentials = DefaultAzureCredential()

subscription_id = "4b5976c6-cdaf-4c73-9c35-78c1086a6502"

compute = ComputeManagementClient(cerdentials, subscription_id)

def deallocate_vm(rgname):

    for vm in compute.virtual_machines.list(rgname):
        tags = vm.tags or {}
        if vm.tags.get('env') == 'dev':
            print(f"stopping the {vm.name} having tag value dev")
            compute.virtual_machines.begin_deallocate(rgname,vm.name)
            vmdetail = compute.virtual_machines.get(rgname,vm.name, expand="instanceView")
            status_object = vmdetail.instance_view.statuses
            for status in status_object:
                if status.code.startswith("PowerState/"):
                    print(f"{vm.name} is in {status.display_status} state")
        
if __name__ == "__main__":

    rgname = input("enter the rg name to stip the vms inside it ").strip()

    deallocate_vm(rgname)



