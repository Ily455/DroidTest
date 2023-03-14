import argparse
import subprocess
import os
import sys


def print_banner():
    os.system("clear") # clear the screen
    print("  _____            _     _ _______        _            ")
    print(" |  __ \          (_)   | |__   __|      | |           ")
    print(" | |  | |_ __ ___  _  __| |  | | ___  ___| |_ ___ _ __ ")
    print(" | |  | | '__/ _ \| |/ _` |  | |/ _ \/ __| __/ _ \ '__|")
    print(" | |__| | | | (_) | | (_| |  | |  __/\__ \ ||  __/ |   ")
    print(" |_____/|_|  \___/|_|\__,_|  |_|\___||___/\__\___|_|   ")

    print()
    print("made with <3 by Ily455, https://github.com/Ily455")
                                                                                       
if __name__ == "__main__":
    print_banner()


def run_adb_commands(
    commands,
    verbose=False,
    verbose_file=None,
    success_file=None,
    fail_file=None,
    success_only=False,
    fail_only=False,
):
    successes = []
    failures = []
    for command in commands:
        adb_command = ["adb"] + command.split()
        result = subprocess.run(
            adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        # print(result.returncode)
        # print(result.stderr)
        #print(result.stdout)
        print()
        if result.returncode != 0:
            failures.append((command, result.stderr.strip()))
            if not success_only and fail_file:
                with open(fail_file, "a") as f:
                    f.write(f"FAIL: {command}\n")
                    f.write(result.stderr)
        else:
            successes.append((command, result.stdout.strip()))
            if verbose or (not fail_only and success_file):
                if not success_only:
                    print(f"PASS: {command}")
                    print(result.stdout)
                if verbose_file:
                    with open(verbose_file, "a") as f:
                        f.write(f"PASS: {command}\n")
                        f.write(result.stdout)
                if not fail_only and success_file:
                    with open(success_file, "a") as f:
                        f.write(f"PASS: {command}\n")
                        f.write(result.stdout)
    # print(successes)
    # print(failures)
    if not success_only and not fail_only:
        print("Results:")
        for command, output in successes:
            # if command in successes:
                print(f"PASS: {command}\n")
        for command, output in failures:
            # elif command in failures:
                print(f"FAIL: {command}\n")
            # result = 'PASS' if command in successes else 'FAIL'
    elif success_only:
        print(f"Successful results ({len(successes)}):")
        for command, output in successes:
            print(f"PASS: {command}")
    elif fail_only:
        print(f"Failed results ({len(failures)}):")
        for command, output in failures:
            print(f"FAIL: {command}")

    if fail_file:
        with open(fail_file, "a") as f:
            f.write("\n".join([f"{command}\n{output}\n" for command, output in failures]))
    return successes, failures


# Parse command line arguments
parser = argparse.ArgumentParser(description="Run ADB commands to test some Android devices functionalities.")
parser.add_argument(
    "-v", "--verbose", action="store_true", help="show verbose output"
)
parser.add_argument(
    "-V",
    "--verbose-file",
    metavar="FILE",
    help="save verbose output to file",
)
parser.add_argument(
    "-s", "--success-file", metavar="FILE", help="save successful output to file"
)
parser.add_argument(
    "-f", "--fail-file", metavar="FILE", help="save failed output to file"
)
parser.add_argument(
    "-S",
    "--success-only",
    action="store_true",
    help="display successful results only",
)
parser.add_argument(
    "-F",
    "--fail-only",
    action="store_true",
    help="display failed results only",
)
args = parser.parse_args()


# List of adb commands to run

filelist = "list.txt"
with open(filelist, "r") as f:
    # read file content and split into a list of strings using newlines as a separator
    adb_commands = f.read().split("\n")
    # print(adb_commands)
# Execute the commands and print status
run_adb_commands(
    adb_commands,
    verbose=args.verbose,
    verbose_file=args.verbose_file,
    success_file=args.success_file,
    fail_file=args.fail_file,
    success_only=args.success_only,
    fail_only=args.fail_only,
)
