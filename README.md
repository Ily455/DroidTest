DroidTester
This script allows you to run multiple ADB commands and display their status. It also provides several options to customize the behavior of the script, such as saving the output to a file or displaying verbose output.


Usage
To use the script, you need to have ADB installed on your system and accessible from the command line. You can run the script with the following command:
python DroidTester.py [-h] [-v] [-V FILE] [-s FILE] [-f FILE] [-n]


Arguments
The script supports the following command line arguments:


-h, --help: show the help message and exit
-v, --verbose: show verbose output for each command
-V FILE, --verbose-file FILE: save verbose output to a file
-s FILE, --save-file FILE: save normal output to a file
-f FILE, --fail-file FILE: save failed output to a file
-n, --count: display the number of successes and failures


Example
Here's an example of how to use the script:



python DroidTester.py -v -V verbose_output.txt -s output.txt -f failed.txt -n



This command will run the script with verbose output, save the verbose output to a file named verbose_output.txt, save all normal output to a file named output.txt, save all failed output to a file named failed.txt, and display the number of successes and failures.


Customization
The script can be customized by modifying the following variables:


adb_commands: a list of ADB commands to run
successes: the number of successful commands
failures: the number of failed commands
verbose: a boolean indicating whether to show verbose output
verbose_file: the name of the file to save verbose output to
success_file: the name of the file to save successful output to
fail_file: the name of the file to save failed output to
normal_file: the name of the file to save normal output to
You can modify these variables to change the behavior of the script to suit your needs.


Contributions
If you find any issues or have suggestions for improving the script, please feel free to open an issue or submit a pull request on GitHub.

