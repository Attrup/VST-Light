class Channel:
    """
    Class representing a single output channel of the VLP light controller.
    """

    def __init__(self):
        """
        Initialize the channel with a default PMW value of 0
        """

        self.intensity = 0
        self.on = False

    def set(self, value: int):
        """
        Set the intensity of the channel. Only 8 bit values are allowed (0-255) and 
        the set function will return an error if the value is outside this range.

        Args:
        -----
            value (int): The value to set the channel to.
        """
        if not 0 < value < 255:
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