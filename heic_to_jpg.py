#!/usr/bin/python3.10
import os
import subprocess
import argparse
import shutil

heic_folder = "heic_files"
no_folders = False
debug_mode = False
sudo_mode = False
step_print = 25
convert_types = [".jpg",".png"]

def get_file_count(curr_path: str) -> int:
    num_files_to_convert = 0
    for filename in os.listdir(curr_path):
        if filename.lower().endswith(".heic"):
            num_files_to_convert += 1
    return num_files_to_convert


def convert_files(curr_path: str,conv_type:str):
    debug_folder = "debug/" if debug_mode else ""
    sudo_mode_command = "sudo" if sudo_mode else ""
    if not no_folders:
        os.makedirs(debug_folder+heic_folder, exist_ok=True)
    num_files_converted = 0
    print("Starting conversion from HEIC to JPG")
    try:
        for _, filename in enumerate(os.listdir(curr_path)):
            if filename.lower().endswith(".heic"):
                debug_folder = "debug/" if debug_mode else ""
                if (not subprocess.run([sudo_mode_command, "convert", f"{debug_folder}{filename}", f"{debug_folder}{(filename[0:-5] + conv_type)}"]).returncode):
                    if not no_folders:
                        if subprocess.run([sudo_mode_command, "mv", f"{debug_folder}{filename}", f"{debug_folder+heic_folder}/"]).returncode:
                            print(
                                f"Couldn't move {debug_folder}{filename} to {debug_folder+heic_folder}/")
                    num_files_converted += 1
                    subs_file = num_files_to_convert-num_files_converted
                    if num_files_converted % step_print == 0 and subs_file > 0:
                        print(
                            f"Converted {num_files_converted} files - {subs_file} remaining")
                else:
                    print(f"Couldn't convert {debug_folder}{filename}")
    except PermissionError:
        print("Not enough permissions operate")

    if (not os.listdir(debug_folder+heic_folder)):
        os.rmdir(debug_folder+heic_folder)
    final_type = conv_type.replace('.',"").upper()
    print(f"Finished converting {num_files_converted} images from HEIC to {final_type}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="HEIC-to-JPG",
                                     description="Convert those pesky HEIC images to JPG or other formats")
    parser.add_argument(
        "--nr", help="Disables the creation of the folder containing the HEIC images after conversion", action="store_true")
    parser.add_argument(
        "--debug", help="For debugging the app", action="store_true")
    parser.add_argument(
        "--sm", help="Enables sudo mode for commands", action="store_true")
    parser.add_argument("--type",default=".jpg",help="Defines the type to convert to (Default: .jpg)",choices=[convert_types])
    args = parser.parse_args()

    no_folders = args.nr
    debug_mode = args.debug
    sudo_mode = args.sm
    curr_path = os.getcwd()
    conv_type = args.type
    if debug_mode:
        os.makedirs("debug", exist_ok=True)
        try:
            for i in range(0, 20):
                shutil.copy(f"{curr_path}/sample1.heic",
                            f"{curr_path}/debug/sample_"+str(i)+".heic")
        except:
            print("Debug files already present")
    debug_folder = "debug/" if debug_mode else ""

    os.chdir(curr_path)
    num_files_to_convert = get_file_count(curr_path+"/"+debug_folder)
    print(f"Found {num_files_to_convert} files to convert")
    if num_files_to_convert > 0:
        step_print = round(num_files_to_convert*0.10)
        if step_print <= 0:
            step_print = 1
        if debug_mode:
            print("DEBUG MODE")
            
            convert_files(f"{curr_path}/debug",conv_type)
        else:
            convert_files(curr_path,conv_type)
