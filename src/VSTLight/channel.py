class Channel:
    """
    Class representing a single output channel of the VLP light controller.
    """

    def __init__(self) -> None:
        """
        Initialize the channel object with a default value of 0 and off state.
        """

        self.__intensity = 0
        self.__on = False

    def set_intensity(self, value: int) -> None:
        """
        Set the intensity of the channel. Only 8 bit values are allowed (0-255) and
        the set function will return an error if the value is outside this range.

        Args:
        -----
            value (int): The value to set the channel to.
        """
        if not 0 <= value <= 255:
            raise ValueError("Channel intensity must be between 0 and 255")

        self.intensity = value

    def get(self) -> int:
        """
        Get the current intensity of the channel.

        Returns:
        --------
            int: The current intensity of the channel.
        """
        return self.intensity
