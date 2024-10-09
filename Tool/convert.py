import subprocess
import platform
import json
from pathlib import Path
import os
# 构造命令
def convert(x,y,z):
    j=['j-x','x-j']
    os_name = platform.system().lower()
    arch = platform.machine().lower()
    if os_name == "darwin":
        if arch == "x86_64":
            binary_path = "./xbs-darwin-amd64"
        elif arch == "arm64" or arch == "aarch64":
            binary_path = "./xbs-darwin-arm64"
        else:
            print(f"Unsupported architecture for Darwin: {arch}")
            return
    elif os_name == "linux":
        if arch == "x86_64":
            binary_path = "./xbs-linux-amd64"
        elif arch == "arm64" or arch == "aarch64":
            binary_path = "./xbs-linux-arm64"
        else:
            print(f"Unsupported architecture for Linux: {arch}")
            return
    else:
        print(f"Unsupported platform: {os_name}-{arch}")
       
    command = [binary_path, j[z], "-i", x, "-o", y]
    # print(command)
    result = subprocess.run(command, capture_output=True, text=True)
    exit_code = result.returncode
    if exit_code != 0:
        print(f"Command failed with exit code {exit_code}")
    else:
        print("Command executed successfully")
def write_json(data, folder ,file_path):
    Path(folder).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(folder, file_path), 'w') as file:
        json.dump(data, file, ensure_ascii=False,indent=4)


def classify_data(data_path):
    with open(data_path, "r") as f:
        data = json.load(f)
        video_list = {}
        comic_list = {}
        audio_list = {}
        text_list = {}
        for key ,value in data.items():
            try:
                if data[key]['sourceType']=='video':
                    video_list[key] = data[key]
                    write_json(data[key],'xbs_source/video',key+'.json')
                    convert('xbs_source/video/'+key+'.json','xbs_source/video/'+key+'.xbs',0)
                elif data[key]['sourceType']=='comic':
                    comic_list[key]=data[key]
                    write_json(data[key],'xbs_source/comic',key+'.json')
                    convert('xbs_source/comic/'+key+'.json','xbs_source/comic/'+key+'.xbs',0)
                elif data[key]['sourceType']=='audio':
                    audio_list[key]=data[key]
                    write_json(data[key],'xbs_source/audio',key+'.json')
                    convert('xbs_source/audio/'+key+'.json','xbs_source/audio/'+key+'.xbs',0)
                elif data[key]['sourceType']=='text':
                    text_list[key]=data[key]
                    write_json(data[key],'xbs_source/text',key+'.json')
                    convert('xbs_source/text/'+key+'.json','xbs_source/text/'+key+'.xbs',0)
            except KeyError:
                data[key]['sourceType'] = 'text'
                text_list[key]=data[key]
                write_json(data[key],'xbs_source/text',key+'.json')
                convert('xbs_source/text/'+key+'.json','xbs_source/text/'+key+'.xbs',0)
        write_json(video_list,'xbs_source/video', 'videoList.json')
        write_json(comic_list,'xbs_source/comic', 'comicList.json')
        write_json(audio_list, 'xbs_source/audio', 'audioList.json')
        write_json(text_list, 'xbs_source/text','textList.json')

def convert_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.xbs'):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.splitext(input_path)[0] + '.json'
            convert(input_path, output_path, 1)
            classify_data(output_path)
def main():
    folder_path = 'xbs_source'
    convert_files_in_folder(folder_path) 

if __name__ == '__main__':
    main()