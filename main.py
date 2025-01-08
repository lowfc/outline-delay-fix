import subprocess
import sys
from typing import Optional
import wmi

"""

This script is needed to determine the network adapter for Internet access and compare its Interface Index parameter 
with the corresponding parameter of the Outline client interface.

Use it only on windows, run it with administrator rights

https://github.com/Jigsaw-Code/outline-apps/issues/1235

"""


POWERSHELL_PATH = r"C:\Windows\system32\WindowsPowerShell\v1.0\powershell.exe"
WMI = wmi.WMI()


def execute_command(args: list) -> Optional[str]:
    try:
        result = subprocess.check_output([POWERSHELL_PATH, *args])
        if result:
            return result.decode(encoding="windows-1251")
    except Exception as e:
        print(f"Caught {e.__class__.__name__}")


def get_user_actual_adapter():
    # IPConnectionMetric = Interface Metric
    result = []
    for adapter in WMI.Win32_NetworkAdapterConfiguration(IPEnabled=True):
        if (
            hasattr(adapter, 'InterfaceIndex') and
            hasattr(adapter, 'IPConnectionMetric') and
            hasattr(adapter, 'DefaultIPGateway') and
            adapter.DefaultIPGateway
        ):
            bro = {
                "InterfaceIndex": adapter.InterfaceIndex,
                "IPConnectionMetric": adapter.IPConnectionMetric,
                'DefaultIPGateway': adapter.DefaultIPGateway
            }
            if hasattr(adapter, 'Description'):
                bro["Description"] = adapter.Description
            else:
                bro["Description"] = "<No name adapter>"
            result.append(bro)
    if len(result) == 0:
        return None
    elif len(result) == 1:
        return result[0]
    else:
        print("We found more than one adapter.")
        print("Please specify the number of the adapter that you use to access the Internet.")
        choose_adapter = None
        for i in range(10):
            for n, adp in enumerate(result):
                print(f"{n + 1}.", adp["Description"], f"(gateways = {adp['DefaultIPGateway']})")
            choose = input("Enter the number of adapter: ")
            try:
                choose_int = int(choose.strip())
            except Exception:
                choose_int = 0
            if choose_int < 1 or choose_int > len(result):
                print("You entered an incorrect number, please try again.")
                continue
            choose_adapter = result[choose_int - 1]
            break
        return choose_adapter


# IPv4 only
def get_interface_index_and_metric(
    interface_name: Optional[str] = None,
    interface_index: Optional[int] = None
) -> Optional[tuple]:
    filter_rule = None
    if interface_index:
        filter_rule = "{ $_.InterfaceIndex -eq " + str(interface_index) + " -and $_.AddressFamily -eq 'IPv4' }"
    elif interface_name:
        filter_rule = "{ $_.InterfaceAlias -like '" + interface_name + "*' -and $_.AddressFamily -eq 'IPv4' }"

    if not filter_rule:
        return None

    result = execute_command(["Get-NetIPInterface | Where-Object",
                              filter_rule,
                              "| Select-Object -Property InterfaceMetric, InterfaceIndex ",
                              "| ConvertTo-Csv -NoTypeInformation"]
                             )
    if not result:
        return None
    try:
        parts = result.split("\n")
        metric, index = parts[1].split(",")
        metric = metric.replace('"', '')
        index = index.replace('"', '')
        index = index.replace('\r', '')
        index = index.replace('\n', '')
        return int(index.strip()), int(metric.strip())
    except Exception as e:
        print(f"Caught {e.__class__.__name__}")


def set_interface_metric(interface_index: int, interface_metric: int):
    execute_command([
        "Set-NetIPInterface",
        f"-InterfaceIndex {interface_index}",
        f"-InterfaceMetric {interface_metric}"
    ])


if __name__ == "__main__":
    # Check powershell is available
    res_check = execute_command(["ls"])
    if not res_check:
        print("We can't find your default PowerShell path =(")
        POWERSHELL_PATH = input("Enter the path to the PowerShell executable file: ")
        res_check = execute_command(["ls"])
    if not res_check:
        print("We can't find your default PowerShell path =(")
        print("Exited.")
        sys.exit(1)

    print("Hello, let's check your environment")
    print("Looking for your adapter", end="\n\n")
    net_adapter = get_user_actual_adapter()
    if not net_adapter:
        print("Can't get your adapter, sorry")
        sys.exit(1)
    print("=" * 20)
    print("ADAPTER NAME:", net_adapter["Description"])
    print("ADAPTER INTERFACE INDEX:", net_adapter["InterfaceIndex"])
    print("ADAPTER INTERFACE METRIC:", net_adapter["IPConnectionMetric"])
    print("=" * 20, end="\n\n")
    print("All ok, now checking the Outline interface.", end="\n\n")
    outline_interface = get_interface_index_and_metric(interface_name="outline-")
    if not outline_interface:
        print("Can't get your outline interface, sorry")
        sys.exit(1)
    print("=" * 20)
    print("OUTLINE INTERFACE INDEX:", outline_interface[0])
    print("OUTLINE INTERFACE METRIC:", outline_interface[1])
    print("=" * 20, end="\n\n")
    print("Everything is ready, check the parameters.", end="\n\n")

    if outline_interface[1] >= net_adapter["IPConnectionMetric"]:
        print(outline_interface[1], ">=", net_adapter["IPConnectionMetric"])
        print("Outline have greater (or equal) Interface Metric, fixing...", end="\n\n")
    else:
        print(outline_interface[1], "<", net_adapter["IPConnectionMetric"])
        print("Everything is fine as it is. Maybe you have problems with your internet connection speed?")
        print("Try to measure the internet connection speed on the https://speedtest.net/ "
              "or contact your internet service provider or VPN service provider.")
        sys.exit(0)

    new_adapter_metric = outline_interface[1] + 10
    print(f"Will set new params for {net_adapter['Description']}: "
          f"InterfaceMetric {net_adapter['IPConnectionMetric']} => {new_adapter_metric}")
    if input("Type 'y' to continue: ").strip() != "y":
        print("Cancelled by user")
        sys.exit(0)
    print("Set new parameters...")
    set_interface_metric(net_adapter["InterfaceIndex"], new_adapter_metric)
    print("Checking is it successfully", end="\n\n")
    new_adapter_params = get_interface_index_and_metric(interface_index=net_adapter["InterfaceIndex"])
    if not new_adapter_params or new_adapter_params[1] != new_adapter_metric:
        print("\n")
        print("Couldn't make changes. Are you sure you started the program with administrator rights?")
    else:
        print("Happy hacking!", end="\n\n")
        print("We have changed the Interface Metric. Restart your computer and everything should work fine.")
        print("If this script helped you, please give us the star.", end="\n\n")
        print("https://github.com/lowfc/outline-delay-fix")
    print("\n")
    input("Press enter to exit the program...")
