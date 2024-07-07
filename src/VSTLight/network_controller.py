import socket
from .channel import Channel


def validate_ip_format(ip: str) -> bool:
    """
    Validate the format of an IP address by checking the following:
    - The IP address must contain 3 dots separating the subnets
    - Each subnet of the IP address must be between 1 and 3 characters long
    - Each subnet of the IP address must be a value between 0 and 255

    Args:
    -----
        ip (str): The IP address to validate.

    Returns:
    --------
        bool: True if the IP address is valid, False otherwise.
    """

    return (
        ip.count(".") == 3
        and all(0 < len(val) <= 3 for val in ip.split("."))
        and all(0 <= int(val) < 256 for val in ip.split("."))
    )


class NetworkController:
    """
    Class representing a VLP light controller. This class is responsible for sending
    commands to the controller and verifying the success by evaluating the responses
    from the unit.
    """

    def __init__(self, channels: int, ip: str = "192.168.11.20") -> None:
        """
        Initialize the NetworkController object and connect to the controller itself.
        Init will throw ValueErrors if the IP address is invalid or the specified
        number of channels is not supported by the controller. If the controller
        is unreachable a ConnectionError will be thrown.

        Args:
        -----
            channels (int): The number of channels the controller should have.
                            Must be between 2 and 4.
            ip (str): The IP address of the controller. Defaults to the native
                      IP address of the VLP controllers.
        """
        # Validate arguments
        if not validate_ip_format(ip):
            raise ValueError(f"Invalid IP address: {ip}")

        if channels not in [2, 3, 4]:
            raise ValueError(
                f"Invalid number of channels: {channels}. Must be between 2 and 4."
            )

        # Validate number of channels
        # Set internal variables and create socket
        self.__ip = ip
        self.__channels = [Channel() for _ in range(channels)]
        self.__port = 1000
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.settimeout(1)

        # Connect to the controller
        try:
            self.__sock.connect((self.__ip, self.__port))
        except Exception as e:
            raise ConnectionError(
                f"Failed to connect to controller with ip: {ip}"
            ) from e

        # Initialize all controller channels to 0 and verify that
        # the controller has the expected number of channels
        for i in range(channels):
            self.__send_command(f"{i:02}F000")
            self.__send_command(f"{i:02}L000")
            # TODO: Verify the response from the controller is OK

    def __send_command(self, command: str) -> str:
        """
        Send a command to the controller and return the response.

        Args:
        -----
            command (str): The command to send to the controller.

        Returns:
        --------
            str: The response from the controller.
        """

        # Add header (@) and calculate checksum
        command = f"@{command}"
        checksum = sum(ord(char) for char in command) % 256

        # Add lowest byte of checksum and delimiter (<CR><LF>) to command
        command += f"{checksum:02X}\r\n"

        self.__sock.sendall(command.encode(encoding="ascii"))
        return self.__sock.recv(16).decode(encoding="ascii")

    def set_value(self, channel_id: int, value: int) -> None:
        """
        Set the intensity of a channel on the controller.

        Args:
        -----
            channel (int): The channel to set the intensity of. Must be between 0 and the number of channels - 1.
            value (int): The intensity to set the channel to. Must be between 0 and 255.
        """
        # Validate arguments
        if not 0 <= channel_id < (len(self.__channels) - 1):
            raise ValueError(
                f"Channel ID must be between 0 and {len(self.__channels) - 1}"
            )

        if not 0 <= value <= 255:
            raise ValueError("Channel intensity must be between 0 and 255")

        # Update the stored channel intensity and send the command
        self.__channels[channel_id].set(value)
        self.__send_command(f"{channel_id:02}L{value:03}")
    
    def set_on(self, channel_id: int) -> None:
        """
        Set the state of a channel on the controller.

        Args:
        -----
            channel (int): The channel to set the state of. Must be between 0 and the number of channels - 1.
        """
        # Validate arguments
        if not 0 <= channel_id < (len(self.__channels) - 1):
            raise ValueError(
                f"Channel ID must be between 0 and {len(self.__channels) - 1}"
            )

        # Update the stored channel state and send the command
        self.__channels[channel_id].on = True
        self.__send_command(f"{channel_id:02}L001")
