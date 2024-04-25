#!/usr/bin/python3.10
import os,subprocess
if __name__ == "__main__":
    curr_path = os.getcwd()
    os.chdir(curr_path)
    heic_folder = "heic_files"
    noFiles = True
    num_files_to_convert = 0
    for filename in os.listdir(curr_path):
        if filename.lower().endswith(".heic"):
            num_files_to_convert+=1

    if(num_files_to_convert > 0):
        os.makedirs(heic_folder,exist_ok=True)
        num_files_converted = 0
        print("Starting conversion from HEIC to JPG")
        for i,filename in enumerate(os.listdir(curr_path)):
            if filename.lower().endswith(".heic"): 
                noFiles = False
                subprocess.run(["sudo","convert", f"{filename}", f"{(filename[0:-5] + '.jpg')}"])
                subprocess.run(["sudo","mv",f"{filename}",f"{os.path.join(curr_path,heic_folder)}"])
                num_files_converted+=1
                if num_files_converted % 25 == 0:
                    print(f"Converted {num_files_converted} files - {num_files_to_convert-num_files_converted} remaining")
        if(not os.listdir(heic_folder)):
            os.rmdir(heic_folder)
        print(f"Finished converting {num_files_converted} images from HEIC to JPG")