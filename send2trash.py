import os
import shutil
import ctypes
import time
import sys

class CleanupStats:
    def __init__(self):
        self.total_files_deleted = 0
        self.total_folders_deleted = 0
        self.total_errors = 0
        self.recycle_bin_empty = False
        self.start_time = time.time()
        self.end_time = None

    def increment_files_deleted(self):
        self.total_files_deleted += 1

    def increment_folders_deleted(self):
        self.total_folders_deleted += 1

    def increment_errors(self):
        self.total_errors += 1

    def set_recycle_bin_empty(self, value):
        self.recycle_bin_empty = value

    def finish_cleanup(self):
        self.end_time = time.time()

    def get_cleanup_duration(self):
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        else:
            return None

    def __str__(self):
        duration = self.get_cleanup_duration()
        duration_str = f"{duration:.2f} seconds" if duration else "N/A"
        
        return f"Cleanup Summary:\n" \
               f"Files Deleted: {self.total_files_deleted}\n" \
               f"Folders Deleted: {self.total_folders_deleted}\n" \
               f"Errors Encountered: {self.total_errors}\n" \
               f"Recycle Bin Emptied: {'Yes' if self.recycle_bin_empty else 'No'}\n" \
               f"Cleanup Duration: {duration_str}"

def empty_temp_folder(folder_path, stats):
    try:
        print(f"Emptying folder: {folder_path}")
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                    stats.increment_files_deleted()
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
                    stats.increment_errors()
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    if dir.startswith('_'):
                        shutil.rmtree(dir_path)
                        print(f"Deleted folder (forcefully): {dir_path}")
                    else:
                        os.rmdir(dir_path)
                        print(f"Deleted directory: {dir_path}")
                    stats.increment_folders_deleted()
                except Exception as e:
                    print(f"Error deleting directory {dir_path}: {e}")
                    stats.increment_errors()
    except Exception as e:
        print(f"Error emptying folder: {e}")
        stats.increment_errors()

def empty_recycle_bin(stats):
    try:
        SHEmptyRecycleBin = ctypes.windll.shell32.SHEmptyRecycleBinW
        flags = 0x01  # SHERB_NOCONFIRMATION
        result = SHEmptyRecycleBin(None, None, flags)
        if result == 0:
            print("Recycle bin emptied successfully.")
            stats.set_recycle_bin_empty(True)
        else:
            print("Error emptying recycle bin.")
            stats.increment_errors()
    except Exception as e:
        print(f"Error emptying recycle bin: {e}")
        stats.increment_errors()

if __name__ == "__main__":
    # Check if the script is run with administrator privileges
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    print("Starting cleanup process...")
    
    cleanup_stats = CleanupStats()

    temp_folder = os.environ.get('TEMP')
    local_temp_folder = os.path.join(os.environ.get('LOCALAPPDATA'), 'Temp')

    if temp_folder:
        empty_temp_folder(temp_folder, cleanup_stats)
    else:
        print("TEMP environment variable not found.")

    if local_temp_folder:
        empty_temp_folder(local_temp_folder, cleanup_stats)
    else:
        print("LOCALAPPDATA environment variable not found.")

    empty_recycle_bin(cleanup_stats)
    
    cleanup_stats.finish_cleanup()
    print("Cleanup process completed.")
    print(cleanup_stats)
    time.sleep(10)
