#!/usr/bin/python3.10
import os
import argparse
import shutil
import pillow_heif
from PIL import Image
heic_folder = "heic_files"
no_folders = False
debug_mode = False
step_print = 25
convert_types = [".jpg", ".png"]
conv_path = "."

def get_file_count(curr_path: str) -> int:
    return len(list(filter(lambda file: file.lower().endswith(".heic"),os.listdir(curr_path))))

def filter_images(files:list[str])->list[str]:
    return list(filter(lambda img: img.lower().endswith(".heic"),files))

def print_conversion_result(num_files_to_convert: int, num_files_converted: int,):

    subs_file = num_files_to_convert-num_files_converted
    if num_files_converted % step_print == 0 and subs_file > 0:
        print(
            f"Converted {num_files_converted} files - {subs_file} remaining")


def convert_files(curr_path: str, conv_type: str):
    if not no_folders:
        os.makedirs(os.path.join(curr_path,heic_folder), exist_ok=True)
    num_files_converted = 0
    print("Starting conversion from HEIC to JPG")
    images = filter_images(os.listdir(curr_path))   
    try:
        for _, filename in enumerate(images):
        
            heic_img = pillow_heif.read_heif(os.path.join(curr_path,filename))
            try:
                img = Image.frombytes(
                    heic_img.mode, heic_img.size, heic_img.data, "raw")
            except:
                print(f"Error converting {os.path.join(curr_path,filename)}")
            else: 
                try: 
                    img.save(f"{os.path.join(curr_path,(filename[0:-5] + conv_type))}")
                except OSError:
                    print(f"Error while trying to save {curr_path}{(filename[0:-5] + conv_type)}")
                if not no_folders:
                    try:
                        shutil.move(os.path.join(curr_path,filename),
                                    os.path.join(curr_path,heic_folder))
                    except shutil.Error:
                        print(f"Couldn't move {curr_path}{filename} to {os.path.join(curr_path,heic_folder)}")
                num_files_converted += 1
                print_conversion_result(
                    num_files_to_convert, num_files_converted)
    except PermissionError:
        print("Not enough permissions operate")
    except:
        print("An error has occured")

    if not no_folders:
        if (not os.listdir(os.path.join(curr_path,heic_folder))):
            os.rmdir(os.path.join(curr_path,heic_folder))
    final_type = conv_type.replace('.', "").upper()
    print(
        f"Finished converting {num_files_converted} images from HEIC to {final_type}")
    return num_files_converted


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="HEIC-to-JPG",
                                     description="Convert those pesky HEIC images to JPG or other formats")
    parser.add_argument(
        "--nr", help="Disables the creation of the folder containing the HEIC images after conversion", action="store_true")
    parser.add_argument(
        "--debug", help="For debugging the app", action="store_true")
    parser.add_argument("--type", default=".jpg",
                        help="Defines the type to convert to (Default: .jpg)", choices=[convert_types])
    parser.add_argument("--path", default=".",
                        help="Specify a path to convert files at")
    args = parser.parse_args()

    no_folders = args.nr
    debug_mode = args.debug
    conv_type = args.type
    conv_path = args.path

    if debug_mode:
        conv_path = "./debug"
        os.makedirs(conv_path, exist_ok=True)
        try:
            for i in range(0, 20):
                shutil.copy(f"{conv_path}/../sample1.heic",
                            f"{conv_path}/sample_"+str(i)+".heic")
        except:
            print("Debug files already present")

    if os.path.exists(conv_path):
        num_files_to_convert = get_file_count(conv_path)
        print(f"Found {num_files_to_convert} files to convert")
        if num_files_to_convert > 0:
            step_print = round(num_files_to_convert*0.10)
            if step_print <= 0:
                step_print = 1
            if debug_mode:
                print("DEBUG MODE")
                conv_path = "debug/"
                convert_files(conv_path,conv_type)
            else:
                convert_files(conv_path, conv_type)
    else:
        print(f"{conv_path} doesn't exist")
