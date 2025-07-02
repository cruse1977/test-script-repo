from dcim.choices import DeviceStatusChoices
from dcim.models import ConsolePort, Device, PowerPort
from extras.scripts import Script


class DeviceConnectionsReport(Script):
    description = "Validate the minimum physical connections for each device"

    def test_console_connection(self):

        # Check that every console port for every active device has a connection defined.
        active = DeviceStatusChoices.STATUS_ACTIVE
        for console_port in ConsolePort.objects.prefetch_related('device').filter(device__status=active):
            if not console_port.connected_endpoints:
                self.log_failure(
                    f"No console connection defined for {console_port.name}",
                    console_port.device,
                )
            elif not console_port.connection_status:
                self.log_warning(
                    f"Console connection for {console_port.name} marked as planned",
                    console_port.device,
                )
            else:
                self.log_success("Passed", console_port.device)

    def test_power_connections(self):

        # Check that every active device has at least two connected power supplies.
        for device in Device.objects.filter(status=DeviceStatusChoices.STATUS_ACTIVE):
            connected_ports = 0
            for power_port in PowerPort.objects.filter(device=device):
                if power_port.connected_endpoints:
                    connected_ports += 1
                    if not power_port.path.is_active:
                        self.log_warning(
                            f"Power connection for {power_port.name} marked as planned",
                            device,
                        )
            if connected_ports < 2:
                self.log_failure(
                    f"{connected_ports} connected power supplies found (2 needed)",
                    device,
                )
            else:
                self.log_success("Passed", device)
