#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import zipfile

from subprocess import call, DEVNULL


tools_path = "tools"
i = 1
# dex2jar_path = tools_path + "/dex2jar/d2j-dex2jar.sh"
# jd_path = tools_path + "/jd-cli/jd-cli"
apktool_path = "/usr/local/bin/apktool"


def decompile_apk(apk_path, output_path, verbose, odex_file=None):
    print("[+] Decompiling the apk\n")

    if verbose:
        stdout = None
        stderr = None
    else:
        stdout = DEVNULL
        stderr = DEVNULL

    if not os.path.exists(apk_path):
        print("[-] Error: couldn't find the apk!")
        return

    apk_name = os.path.splitext(os.path.basename(apk_path))[0]

    if os.path.exists("temp"):
        print("[~] Removing old temp directory")
        shutil.rmtree("temp")

    print("[+] Creating temp directory")
    os.makedirs("temp")

    apk_zip = "temp/" + apk_name + ".zip"
    shutil.copy2(apk_path, apk_zip)

    apk_unziped_dir = "temp/" + apk_name + "_unziped"
    os.makedirs(apk_unziped_dir)
    try:
        zip_ref = zipfile.ZipFile(apk_zip, 'r')
        zip_ref.extractall(apk_unziped_dir)
        zip_ref.close()
    except: 
        pass
    apk_classes = apk_unziped_dir + "/classes.dex"
    # if odex_file is not None:
    #     apk_classes = odex_file

    if not os.path.exists(apk_classes):
        print("[-] Error: the apk doesn't have the classes.dex")
        return

    # print("[+] Getting the jar")
    # apk_jar = "temp/" + apk_name + ".jar"
    # call(dex2jar_path + " " + apk_classes + " -o " + apk_jar,
    #      stdout=stdout, stderr=stderr, shell=True)

    # print("[+] Decompiling the jar")
    #apk_java = "temp/" + apk_name + "_java/src"
    # call(jd_path + " " + apk_jar + " -od " + apk_java,
    #      stdout=stdout, stderr=stderr, shell=True)

    # print("[+] Reverse engineering the apk")
    # apk_re = "temp/" + apk_name + "_re"
    # call(apktool_path + " d " + apk_path + " -o " + apk_re,
    #      stdout=stdout, stderr=stderr, shell=True)

    # print("[+] Organizing everything")
    # output_dir = os.path.join(output_path, apk_name)
    # if os.path.exists(output_dir):
    #     shutil.rmtree(output_dir)
    # os.makedirs(output_dir)

    # print("[+] Moving reverse engineering files")
    # re_list = os.listdir(apk_re)
    # for re_files in re_list:
    #     shutil.move(os.path.join(apk_re, re_files), output_dir)
    global i
    print("[+] Moving Dex files")
    if os.path.exists("boqx_dex_files"):
        if os.path.exists("boqx_dex_files" + "/classes.dex"):
            new_name = "boqx_dex_files/classes_" + str(i) + ".dex"
            shutil.copy(apk_classes, new_name)
            i = i+1
        else:
            shutil.copy(apk_classes, "boqx_dex_files")


    if os.path.exists("temp"):
        print("[~] Removing temp directory")
        shutil.rmtree("temp")

    print("\n[+] Done decompiling the apk")


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--apk", help="Apk file",
                        required=False)

    parser.add_argument("-o", "--output-dir", help="Output directory",
                        required=False, default=".")

    parser.add_argument("-x", "--odex-file", help="Specify odex file",
                        required=False)

    parser.add_argument("-v", "--verbose", help="Enables verbose",
                        required=False, action="store_true", default=False)

    return parser.parse_args()


def verify_tools():
    # if not os.path.exists(dex2jar_path):
    #     print("[-] Error: 'dex2jar' it's missing from the tools directory")
    #     return False

    # if not os.path.exists(jd_path):
    #     print("[-] Error: 'jd-cli' it's missing from the tools directory")
    #     return False

    if not os.path.exists(apktool_path):
        print("[-] Error: 'apktool' it's missing from the tools directory")
        return False

    return True

import os
sample_dir_path = "Android_Family_dataset/boqx/boqx_samples/"
sample_files_path = []
def main():
    for root, dir, files in os.walk(sample_dir_path):
        for filename in files:
            sample_files_path .append(sample_dir_path + filename)
        
    args = get_args()

    # # if not verify_tools():
    # #     print("Please check if all the tools are in the 'tools' directory")
    # #     print("and if all the tools have the permission to be executable.\n")

    # #     print("You can give permissions to the tools with this command: ")
    # #     print("sudo chmod -R +x tools")
    # #     return
    for apk_file in sample_files_path:
        decompile_apk(apk_file, args.output_dir, args.verbose,
                  odex_file=args.odex_file)
    #print(sample_files_path)

if __name__ == "__main__":
    main()