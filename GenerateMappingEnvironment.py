import os
from os.path import isfile, join
from shutil import copy, copytree
import subprocess

from ErrorLog import ErrorLog

common_file_path = os.getcwd() + "/common_files"

class GitRepo:
    def __init__(self, project, host="git@github.com", organization="Starcounter"):
        self.host = host
        self.organization = organization
        self.project = project

    def __init__(self, host="git@github.com", organization="Starcounter"):
        self.host = host
        self.organization = organization
        self.project = ""

    def SetProject(self, project):
        self.project = project

    def GitPath(self):
        return self.host + ":" + self.organization + "/" + self.project

def GenerateMappingEnvironment(dir_path = "c:/Starcounter/AppName", git_repo = GitRepo()):
    error_log = ErrorLog()
    app_name = dir_path.split('/')[-1]
    mapping_dir_path = join(dir_path, 'src', app_name + ".Mapper")
    replaceable_dir_path = join(common_file_path, 'replaceable')

    git_repo.SetProject(app_name)

    if not os.path.exists(mapping_dir_path):
        try:
            os.makedirs(mapping_dir_path)
        except OSError:
            error_log.LogError("Creation of Mapper directory failed.  Check permissions and try again")
            return

    AddMainDirCommonFile(mapping_dir_path)
    AddCustomFile(replaceable_dir_path, 'AppName.Mapper.csproj', app_name, mapping_dir_path)
    AddSharedSubmodule(mapping_dir_path)
    AddMapperProjToSolution(app_name, dir_path)

def AddMainDirCommonFile(dst_path):
    dir_contents = os.listdir(common_file_path)
    for f in dir_contents:
        src_path = join(common_file_path, f)
        if isfile(src_path):
            copy(src_path, dst_path)
    return

def AddCustomFile(src_dir, file_name, replace_value, dst_dir):
    error_log = ErrorLog()
    orig_file_path = join(src_dir, file_name)
    if not os.path.exists(orig_file_path):
        error_log.LogError("Common file template not found")
        return
    dst_file_path = join(dst_dir, file_name)
    if file_name.find('AppName') != -1:
        dst_file_path = join(dst_dir, file_name.replace('AppName', replace_value))
    try:
        with open(orig_file_path) as orig_file:
            dst_file = open(dst_file_path, 'w+')
            dst_file.write(orig_file.read().replace('%REPLACE%', replace_value))
            dst_file.close()
    except OSError:
        error_log.LogError("Unable to create custom file " + file_name + " with replace value " + replace_value)


def AddSharedSubmodule(mapping_dir_path):
    error_log = ErrorLog()
    bat_file_path = join(mapping_dir_path, 'add_shared.bat')
    try:
        subprocess.call([bat_file_path])
    except:
        error_log.LogError("Unable to add shared submodule")
    os.remove(bat_file_path)
    return

def AddMapperProjToSolution(proj_name, root_dir):
    error_log = ErrorLog()
    bat_file_path = join(root_dir, 'add_project.bat')
    AddCustomFile(join(common_file_path, 'replaceable'), 'add_project.bat', proj_name, root_dir)
    try:
        subprocess.call([bat_file_path])
    except:
        error_log.LogError("Unable to fix sln for " + proj_name + " Project")
    FixStupidSolutionFile(proj_name, root_dir)
    os.remove(bat_file_path)

def FixStupidSolutionFile(proj_name, root_dir):
    error_log = ErrorLog()
    temp_sln_file_path = join(root_dir, proj_name + "_temp.sln")
    sln_file_path = join(root_dir, proj_name + ".sln")
    os.rename(sln_file_path, temp_sln_file_path)
    try:
        with open(temp_sln_file_path) as sln_file:
            output_file = open(sln_file_path, 'w+')
            for line in sln_file:
                if line.find('"src", "src",') != -1:
                    sln_file.readline()
                elif line.find('GlobalSection(NestedProjects) = preSolution') != -1:
                    sln_file.readline()
                    sln_file.readline()
                else:
                    output_file.write(line)
            output_file.close()
    except OSError:
        error_log.LogError("Unable to fix " + proj_name + " solution file")
        return
    os.remove(temp_sln_file_path)

error_log = ErrorLog()
error_log.ClearErrorLog()
GenerateMappingEnvironment()




