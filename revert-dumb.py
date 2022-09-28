import getopt
import subprocess
import sys
from time import sleep

import constants


def writeHelp() -> None:
    """Write the help text to the console."""
    print("== Options ==")
    print(
        "-t, --time: amount of time in seconds to wait before",
        "running recovery commands. (10 - 3600, default 120)",
    )
    print(
        "-a, --action: the potentially dumb commands to run",
        "-r, --recovery: the recovery commands to run",
        "==========",
        "-h, --help: Show this help text",
        "-v, --version: Show version information",
        "==========",
        sep="\n",
    )


def writeVersion() -> None:
    """Write the version information to the console."""
    print(
        f"v{constants.VERSION}",
        f"{constants.GITHUB}",
        sep="\n",
    )


def clearline(msg: str) -> None:
    """
    Clear the current line and write a new message.
    Source: https://stackoverflow.com/a/53843296/1482354
    """
    sys.stdout.write(constants.CURSOR_UP_ONE)
    sys.stdout.write(constants.ERASE_LINE + "\r")
    print(msg, end="\r")


def run(time: int, action: str, recovery: str) -> bool:
    """Run the script."""
    print(f"\n=== Running '{action}' ===")
    action_return_code = subprocess.call(action, shell=True)
    if action_return_code != 0:
        print(f"\nAction '{action}' failed with return code {action_return_code}")
        return False

    print(f"\n=== Waiting {time}s ===")
    while time != 0:
        clearline(f"{time}s remaining")
        sleep(1)
        time -= 1
    print("Timed out, running recovery")

    print(f"\n=== Recovering by running '{recovery}' ===")
    recovery_return_code = subprocess.call(recovery, shell=True)
    if recovery_return_code != 0:
        print(
            f"\nRecovery command '{recovery}' failed with",
            f"return code {recovery_return_code}",
        )
        return False

    return True


def main(argv) -> None:
    """Main function."""
    print(f"revert-dumb v{constants.VERSION}", "==========", sep="\n")

    action = False
    time = 120
    recovery = False

    if len(sys.argv) == 1:
        writeHelp()
        sys.exit()
    else:
        try:
            opts, args = getopt.getopt(
                argv, "vha:t:r:", ["version", "help", "action=", "time=", "recovery="]
            )
        except getopt.GetoptError as err:
            print(err)
            writeHelp()
            sys.exit()
        for opt, arg in opts:
            if opt in ("-v", "--version"):
                writeVersion()
                sys.exit()
            elif opt in ("-h", "--help"):
                writeHelp()
                sys.exit()
            elif opt in ("-a", "--action"):
                action = arg
            elif opt in ("-t", "--time"):
                if arg.isdigit():
                    if time > constants.TIME_MAX:
                        print(
                            "Time cannot be greater than",
                            f"{constants.TIME_MAX} seconds.",
                        )
                        sys.exit()
                    elif time < constants.TIME_MIN:
                        print(
                            f"Time cannot be less than {constants.TIME_MIN}",
                            "seconds.",
                        )
                        sys.exit()
                    else:
                        time = int(arg)
                else:
                    print("Time must be a number.")
                    sys.exit()
            elif opt in ("-r", "--recovery"):
                recovery = arg
            else:
                print("unhandled option")
                sys.exit()

        if action and recovery:
            print(
                f"  Action: {action}",
                f"    Time: {time}s",
                f"Recovery: {recovery}",
                sep="\n",
            )
            run(time, action, recovery)
        else:
            print("Incorrect usage!", "Missing action/recovery commands\n", sep="\n")
            writeHelp()
            sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
