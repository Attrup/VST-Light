"""
This example demonstrates how to set the strobe mode of a channel using the VSTLight module.
"""

from VSTLight import NetworkController


def main() -> None:
    # Create controller object
    lights = NetworkController(4)

    # Set strobe modes of two channels
    lights.set_strobe_mode(2, 4)
    lights.set_strobe_mode(4, 10)

    # Trig the channels using the trig input of the light controller unit
    # Below is simply a dummy loop to keep the program running.
    while True:
        if input("Press 'q' to quit") == "q":
            break

    # Close down gracefully
    lights.destroy()


if __name__ == "__main__":
    main()
