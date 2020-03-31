# -*- coding: utf-8 -*-
import argparse
import textwrap
import os

import label_tool
import utils
from config import config

def upload_dataset(image_path,anno_path,project_id,dataset_id,verbose = False):
    utils.check_path_exist(image_path)
    utils.remove_local_file(config["image_tar_name"])
    utils.remove_local_file(config["json_tar_name"])
    cmd = "tar zcf %s %s/*.jpg" % (config["image_tar_name"],image_path)
    if verbose:
        print(cmd)
    os.system(cmd)
    utils.check_path_exist(config["image_tar_name"])
    utils.check_path_exist(anno_path)
    cmd = "tar zcf %s %s/*.json" % (config["json_tar_name"],anno_path)
    if verbose:
        print(cmd)
    os.system(cmd)
    utils.scp(config["identity_file"],config["image_tar_name"], config["nfs_base_path"],config["user"], config["host"])
    utils.scp(config["identity_file"],config["json_tar_name"], config["nfs_base_path"],config["user"], config["host"])
    utils.scp(config["identity_file"],"list.json", config["nfs_base_path"],config["user"], config["host"])
    utils.scp(config["identity_file"],"commit.json", config["nfs_base_path"],config["user"], config["host"])
    target_image_base_path = os.path.join(config["nfs_base_path"],"label/public/tasks",dataset_id)
    target_json_base_path = os.path.join(config["nfs_base_path"],"label/private/tasks",dataset_id,project_id)
    cmd = ""
    cmd += "rm -rf" + os.path.join(target_image_base_path,"images") +";"
    cmd += "rm -f" + os.path.join(target_image_base_path,"list.json") +";"
    cmd += "rm -f" + os.path.join(target_image_base_path,"commit.json") +";"
    cmd += "rm -rf" + os.path.join(target_json_base_path, "images") + ";"
    cmd += "mkdir -p" + target_image_base_path +";"
    cmd += "mkdir -p" + target_json_base_path +";"

    cmd += "tar zxf %s -C %s" %(os.path.join(config["nfs_base_path"],config["image_tar_name"]),target_image_base_path) + ";"
    cmd += "mv %s %s" % (os.path.join(config["nfs_base_path"], "list.json"), target_image_base_path) + ";"
    cmd += "tar zxf %s -C %s" %(os.path.join(config["nfs_base_path"],config["json_tar_name"]),os.path.exists("")) + ";"
    cmd += "mv %s %s" % (os.path.join(config["nfs_base_path"], "commit.json"), target_image_base_path) + ";"
    if verbose:
        print(cmd)
    utils.SSH_exec_cmd_with_output(config["identity_file"],config["user"], config["host"],cmd)

def upload_model_predict_result(anno_path,dataset_id,project_id,verbose = False):
    cmd = "tar zcf %s %s/*.json" % (config["json_tar_name"], anno_path)
    if verbose:
        print(cmd)
    os.system(cmd)
    utils.scp(config["identity_file"], config["json_tar_name"], config["nfs_base_path"], config["user"], config["host"])
    target_json_base_path = os.path.join(config["nfs_base_path"], "label/private/predict", dataset_id, project_id)
    cmd = ""
    cmd += "rm -f" + os.path.join(target_json_base_path, "list.json") + ";"
    cmd += "mkdir -p" + target_json_base_path + ";"
    cmd += "tar zxf %s -C %s" % (os.path.join(config["nfs_base_path"], config["json_tar_name"]), os.path.exists("")) + ";"
    if verbose:
        print(cmd)
    utils.SSH_exec_cmd_with_output(config["identity_file"],config["user"], config["host"],cmd)

def run_command(args, command, nargs, parser):
    if command == "upload_dataset":
        if len(nargs) != 4:
            parser.print_help()
            print("upload_dataset [image_path] [anno_path] [project_id] [dataset_id]")
        else:
            upload_dataset(nargs[0], nargs[1],nargs[2],nargs[3])
    elif command == "upload_model_predict_result":
        if len(nargs) != 3:
            parser.print_help()
            print("upload_model_predict_result [anno_path] [project_id] [dataset_id]")
        else:
            upload_model_predict_result(nargs[0], nargs[1],nargs[2])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='upload.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''\
    upload tools
        
    Command:
        upload_dataset 
            [image_path] [anno_path] [project_id] [dataset_id]
      '''))
    args = parser.parse_args()
    parser.add_argument("command",
                        help="See above for the list of valid command")
    command = args.command
    nargs = args.nargs
    run_command(args, command, nargs, parser)