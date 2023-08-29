# Temporary Files Cleanup Script

This script is designed to help you clean up temporary files and folders from your system, including the Windows Recycle Bin. It can be particularly useful for freeing up disk space and optimizing system performance.

## Usage

1. Make sure you have administrator privileges before running this script.

2. Run the script using a Python interpreter:

python cleanup_script.py

If you're not running the script as an administrator, the script will prompt you for administrative privileges and then continue with the cleanup process.

3. The script will start by emptying the system's temporary folders and the Windows Recycle Bin. It will display messages for each file and folder it deletes.

4. Once the cleanup process is complete, the script will display a summary of the cleanup, including the number of files deleted, folders deleted, errors encountered, whether the Recycle Bin was emptied, and the total cleanup duration.

5. The script will pause for 10 seconds before exiting. You can adjust this delay by modifying the `time.sleep(10)` line in the script.

## Important Note

- Use this script with caution. Deleting files and folders from your system can lead to unintended consequences. Make sure you have a backup of any important data before running the script.

- This script is specifically designed for Windows systems.

## Script Explanation

The script defines a class `CleanupStats` to keep track of cleanup statistics, including the number of files and folders deleted, errors encountered, and the cleanup duration. The main cleanup logic is implemented using the `empty_temp_folder` function to delete files and folders recursively, and the `empty_recycle_bin` function to empty the Recycle Bin using Windows API calls.

The script checks for administrator privileges using the `is_admin` function. If the script is not run with administrator privileges, it will attempt to re-run itself with administrative privileges.

## Disclaimer

This script is provided as-is, without any warranties or guarantees. Use it at your own risk. The author is not responsible for any data loss or system issues that may arise from using this script.

---
*Note: This script is provided for educational and illustrative purposes only. It's important to exercise caution and ensure you understand the actions the script will perform before using it on your system.*
