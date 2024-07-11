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
