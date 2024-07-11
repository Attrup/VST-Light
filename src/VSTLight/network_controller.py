import socket
from .channel import Channel
from .utils import validate_ip_format


class NetworkController:
    """
    Class representing a VLP light controller. This class is responsible for sending
    commands to the controller and verifying the success by evaluating the responses
    from the unit.
    """

    def __init__(self, channels: int, ip: str = "192.168.11.20") -> None:
        """
        Initialize the NetworkController object and connect to the controller itself.
        Init will throw `ValueErrors` if the IP address is invalid or the specified
        number of channels is not supported by the controller. If the controller
        is unreachable a `ConnectionError` will be thrown.

        If the light controller is unreachable at any point during the lifetime of the
        object, function calls will be blocking for up to 5 seconds, before raising a
        `ConnectionError`.

        Args:
        -----
            channels (int): The number of channels the controller object should have. Must be between 1 and 4.
            ip (str): The IP address of the controller. Defaults to the native IP address of the VLP controllers.
        """
        # Validate arguments
        if not validate_ip_format(ip):
            raise ValueError(f"Invalid IP address: {ip}")

        if channels not in [1, 2, 3, 4]:
            raise ValueError(
                f"Invalid number of channels: {channels} - Must be between 1 and 4"
            )

        # Validate number of channels
        # Set internal variables and create socket
        self.__ip = ip
        self.__channels = [Channel() for _ in range(channels)]
        self.__port = 1000
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.settimeout(5)

        # Connect to the controller
        try:
            self.__sock.connect((self.__ip, self.__port))
        except Exception as e:
            raise ConnectionError(
                f"Failed to connect to controller with ip: {ip}"
            ) from e

        # Initialize all controller channels to intensity 0 (off)
        for i in range(channels):
            self.__send_command(f"{i:02}F000")

    def set_intensity(self, channel_id: int, value: int) -> None:
        """
        Set the light intensity of a channel. If the channel is off, the intensity will be set locally but not transmitted
        to the controller. If the channel is on, the intensity will additionally be transmitted to the controller.

        Args:
        -----
            channel (int): The channel to set the intensity of. Corresponds to the channel number on the controller [1-4].
            value (int): The intensity to update the channel with. Only 8 bit values are accepted [0-255].
        """
        # Validate arguments
        self.__verify_channel_id(channel_id)

        if not 0 <= value <= 255:
            raise ValueError("Channel intensity must be between 0 and 255")

        # Convert channel ID to index
        channel_idx = channel_id - 1

        # Update the stored channel intensity and send the command
        self.__channels[channel_idx].intensity = value

        # Update the value on the controller if the channel is on
        if self.__channels[channel_idx].state:
            self.__send_command(f"{channel_idx:02}F{value:03}")

    def set_on(self, channel_id: int) -> None:
        """
        Set the state of a channel on the controller.

        Args:
        -----
            channel (int): The channel to turn on. Corresponds to the channel number on the controller [1-4].
        """
        # Validate arguments
        self.__verify_channel_id(channel_id)

        # Convert channel ID to index
        channel_idx = channel_id - 1

        # Update the stored channel state and send the command
        self.__channels[channel_idx].on()
        self.__send_command(
            f"{channel_idx:02}F{self.__channels[channel_idx].intensity:03}"
        )

    def set_off(self, channel_id: int) -> None:
        """
        Set the state of a channel on the controller.

        Args:
        -----
            channel (int): The channel to turn off. Corresponds to the channel number on the controller [1-4].
        """
        # Validate arguments
        self.__verify_channel_id(channel_id)

        # Convert channel ID to index
        channel_idx = channel_id - 1

        # Update the stored channel state and send the command
        self.__channels[channel_idx].off()
        self.__send_command(f"{channel_idx:02}F000")

    def __verify_channel_id(self, channel_id: int) -> None:
        """
        Verify that a channel ID is valid. Throws a ValueError if the channel ID if not.

        Args:
        -----
            channel_id (int): The channel ID to verify.
        """
        if not 1 <= channel_id <= len(self.__channels):
            raise ValueError(f"Channel ID must be between 1 and {len(self.__channels)}")

    def __send_command(self, command: str) -> None:
        """
        Send a command to the controller in the VLP IP protocol format. This is achieved by adding
        a header (@), checksum, and a delimiter (<CR><LF>) to the command passed to the function,
        before encoding it to ascii bytes and sending it to the controller.

        Args:
        -----
            command (str): The command to send to the controller.
        """

        # Add header (@) and calculate checksum according to the VLP IP protocol
        command = f"@{command}"
        checksum = sum(ord(char) for char in command) % 0xFF

        # Add lowest byte of checksum and delimiter (<CR><LF>) to command
        command += f"{checksum:02X}\r\n"

        self.__sock.send(command.encode(encoding="ascii"))
