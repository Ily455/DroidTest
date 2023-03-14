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
    success_count=False,
    fail_count=False,
    success_file=sys.stdout,
    fail_file=sys.stdout,
):
    successes = 0
    failures = 0
    for command in commands:
        adb_command = ["adb"] + command.split()
        result = subprocess.run(
            adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode != 0:
            failures += 1
            if verbose:
                print(f"FAIL: {command}")
                print(result.stderr)
            if fail_file:
                with open(fail_file, "a") as f:
                    f.write(f"FAIL: {command}\n")
                    f.write(result.stderr)
        else:
            successes += 1
            if verbose:
                print(f"PASS: {command}")
                print(result.stdout)
            if verbose_file:
                with open(verbose_file, "a") as f:
                    f.write(f"PASS: {command}\n")
                    f.write(result.stdout)
            if success_file:
                with open(success_file, "a") as f:
                    f.write(f"PASS: {command}\n")
                    f.write(result.stdout)
    if success_count:
        print(f"Number of successes: {successes}")
    if fail_count:
        print(f"Number of failures: {failures}")


# Parse command line arguments
parser = argparse.ArgumentParser(description="Run ADB commands")
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
    "-n",
    "--count",
    action="store_true",
    help="display number of successes and failures",
)
args = parser.parse_args()


# List of adb commands to run

adb_commands = ['shell input touchscreen tap 40 40',
'shell dumpsys input',
'shell dumpsys sensorservice',
'shell am start -a android.intent.action.VIEW -d \'geo:0,0?q=<latitude>,<longitude>(Label)\'',
'shell am start -a android.settings.WIFI_SETTINGS',
'shell am start -a android.settings.BLUETOOTH_SETTINGS',
'shell input keyevent KEYCODE_VIBRATE',
'shell am start -a android.media.action.IMAGE_CAPTURE',
'shell dumpsys battery',
'shell df',
'shell wm size',
'shell wm density',
'shell ping -c 10 www.google.com',
'shell dd if=/dev/zero of=/sdcard/testfile bs=1024 count=1024',
'shell dd if=/sdcard/testfile of=/dev/null bs=1024 count=1024',
'shell lsusb',
'shell dumpsys nfc',
'shell settings put system flashlight_available 1',
'shell am start -a android.intent.action.MAIN -n com.android.systemui/com.android.systemui.flashlight.FlashlightActivity',
'shell dumpsys proximity',
'shell monkey -p com.android.monkey -v 500',
'shell am start -a android.intent.action.MAIN -n com.android.settings/.DevelopmentSettings',
'shell settings put system accelerometer_rotation 1',
'shell settings put system user_rotation 1',
'shell am start -a android.provider.MediaStore.RECORD_SOUND',
'shell am start -a android.media.action.VIDEO_CAPTURE',
'shell input keyevent 120',
'shell cat /proc/cpuinfo',
'shell dumpsys batteryinfo',
'shell df -h',
'shell am start -a android.settings.WIFI_DISPLAY_SETTINGS',
'shell am start -a android.intent.action.MAIN -n com.android.phone/.NetworkSetting',
'shell getprop',
'shell getenforce'
]




# Execute the commands and print status
run_adb_commands(
    adb_commands,
    verbose=args.verbose,
    verbose_file=args.verbose_file,
    success_count=args.count,
    fail_count=args.count,
    success_file=args.success_file,
    fail_file=args.fail_file,
)
