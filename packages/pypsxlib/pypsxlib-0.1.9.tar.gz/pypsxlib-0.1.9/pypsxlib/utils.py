"""
pypsxlib: Unofficial python library for reading and writing Agisoft Photoscan/Metashape psx project files.

Copyright (c) 2019 Luke Miller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&@@@@@@@%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@@(/****%@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@@@@@&/*,,,,,,*&@@@@@@@@@@@@@@@@@@@@@@@@&@@@@@@@@@*//*****/**//*/#@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@,(*,,,,,,,,*(,,,,,/*,,,,,,,(@@@@@@@@@@@@@@@@@@@@@@@@&*(%(//****************/@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@,,,,***#*,,,,,,,,,,,,,,,,,,,,,*@@@@@@@@@@@@@@@@&@@@@@(********************/(***@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@*,,,,*,*,,*/**(%%&&@@@@@@@@@#/**@@@@@@@@@@@@@@@&@@@@@************##%******(**(.*(@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@#,,,,*,*,,*@(((((((((((((((((%/*@@@@@@@@@@@@@@@@@@@@/*/*%%**/****/#/*****(*/./**&@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@%%@,,,,*,*,,,#(((((((((((((((((@**@@@@@@@@@@@@@@@@@@@@**(&%%/***/&%&(**@&//(***#*@@@@@@@@@@@@@@@
@@@@@@@@@@@@@&@@@@@@@@&@,,,,*,*,*,#(((((((((((((((((@**@@@@@@@@@@@@&@@@@@@@#**(/(//***(%#,/@*#/@/*/(***@@@@@@@@@@@@@@
@@@@@@@@@@@@@&@@@@@@@@@@,,,,*,*,*,%(((((((((((((((((@/*@@@@@@@@@@@@@@@@@@@(**#/****//**%%.(%@*(***@@*****&@@@@@@@@@@@@@
@@@@@@@@@@@@@@@&@@@@@@@@,,,,*,,*,*&(((((((((((((((((@/*@@@@@@@@@@@@@@@@@@@*****(@@@@@@/****//@*****@@****(@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@&&@@@@,,,,,*,*,*@(((((((((((((((((@/*@@@@@@@@@@%@@@@@@@@*****@@@@@@@@((#@@@%******@@/**/@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@*,,,,*,*,/@(((((((((((((((((%/*@@@@@@@@&@@@@@@@@@@****@@@@@@@@#**&**&@@******@@@#@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@/,,,,*,*,,(/%@&&%%%&@@@@@%/*/,*&&&@@@@&@@@@@@%@@@@@//@@@@@@@@@&/%*(%%@@@@&/**@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@(*#,,/,(,,,,,*********,,,,,,,,*@@@@@@&@@@@@@@@@&@@@@@@@@@@@@@@%&%%&@%&@@@@/**@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@((,#*(,%//*********,**////////(@@@@@@@@@@@@&@@@@&@@@@@%@@@@@%%%@@@@@%%%%&@***(@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@/#**#,*,,,,,,,,,,,,,,,,,,,,,,(@@@@@&@@@@@%@@@@@@@@@@@*/&@&%%%%%@@@%%%%%%@****@%@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@/(#,,*&@&%&%%#%&&@@&&&@@@@@@@@@@@@@@@@@&&@@&@@@@%**&%%%%%%%%@&%%%%%%@*****(&@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@%(#*,,,,,,,,,,,,,,,,,,,,,(/@@@@@@@&@@@@@%@@@@@@@@@***@%%%%%%%%@@&%%%%%@*****//@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@/////%////((#@***##%..&(/@///@@@@@@@@@&&@@@@@@@@@@&***#%%%%%%@@@@@@@@@@&%*****/@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@///////&////(...(%%/....*///(#///@@@@@@@@@@@@@@@@@@@/***/@%%%@@@@@@@@@@@%%@&****/@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@*/#////////(//*..*,./.....(%//((***@@@@@@@@@@@@@@@@@&****@@%%%&@@@@@@@@@%%%@@@/**@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@%(@***#///////(@...........&////%*,(@@@@@@@@@@@@@@@@#****@@@@%%%@@@@@@@@&%%%@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@%,,,,*/**%/////#*............&///#,***&@@@@@@@@@@@@@(****@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@,,,,,,,@*&////(&,,(/((/,......(//%,,,,,,#@@@@@@@@@@@***/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@/*,,,*,@//////#@................%#/%,,,,,,,#@@@@@@@@***@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@&,,,,,@@/////////.................%%//*,,,,,,,,,,*%***/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@(,,,,,*@(#/#(//(@................&(#%(@@@@@,,,,,,,%%#**@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@(,,,,,*@#//////#@&%(&@&*...*#@(((%((&(@@@@**/**,#%*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@*,,,,*@@@@&%@@@%(((((((((((((#(#(((((#%(#%@@//#%%#*#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@#,,,,*@@@@@(((((((((((((((%%@#(%(&(((((((/((%@@@@@@@&/%#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@/**,,,,,*@@@@@%(((((((((((((((((((#(((((((((%%(((@@@@@@@@@@@@@@@@@@**/#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@%%*(/,,,(,*@@@@@@@(((((((((((((((((((@((((((((((((((@@@@@@@@@@@@@@@@///(%#***(/%#(/(///%@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@(**&@@@@@@@@@@@@@@@@#((((((((((((((((@((((((((%#%&(*@@@@@@@@@@@@@@&////////#////%/***/@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&((((((((((((#((&@((((((/,,,,,@@@@@@@@@@@@@@/*******/&////////@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%(#(#%(*%%%@@@#((((##%&@@@@@@@@@@@@@*********/****///#@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#((((((((#/,,,/@@@@@&(((%%%%(@@@@@@@@@@@@@/,......%.,*****@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#(((((((((((,(@@@@@@@((((((((%@@@@@@@@@@@@@.......,&...**@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%((((((((((((((#@@@@@@@@@@(((((#((#@@@@@@@@@@@@@@...*****%...@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@(/@(((((((((((@@@@@@@@@@@@@((((&&@@((@@@@@@@@@@@@@@******//(*&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@///(#((((&@@@@@@@@@@@@@@@@@@&@(#(//((@@@@@@@@@@@@@@@///////(#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@&*,,,%/(/#@@@@@@@@@@@@@@@@@@@@@%((#/,*(/%,,,(,,*@@@@@@@@(///***@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@(/%*/*,#/@@@@@@@@@@@@@@@@@@@@@@@@@@@*,*/#*,,,#,,,%&@@@@@@@@%*****.@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@&/(,*(**(@@@@@@@@@@@@@@@@@@@@@@@@@@@###(((///#/@@@@@@@@@@@#%...../@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@%#,,,,,%@@@@@@@@@@@@@@@@@@@@@@@@@@(//@%/%&%@@@@@@@@@@@@@..,*.***@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@&/**,,,,/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@(*,..#***//@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@//#*,,#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@****@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@@@/@(&/@#*.*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@(**&@@@@@@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@**@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@@@@@&%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""

import copy
import warnings
import xml.etree.ElementTree as ET

from pathlib import Path
from zipfile import ZipFile
from pypsxlib import Masks, __version_psx__, Project


def parse_xml(cwd, root, project_name):
    warnings.warn("`parse_xml` is a provisional function and may not exist in future versions.")
    # print out a psx project (call from parse_xmlfile)
    depth = " " * len(Path(cwd).parts)
    if root.text:
        print(depth, root.tag, root.attrib, root.text)
    else:
        print(depth, root.tag, root.attrib)

    if "path" in root.attrib:
        fname = root.attrib["path"]
        fname = fname.replace("{projectname}", project_name)
        fpath = Path(cwd, fname)
        if fpath.suffix == ".zip":
            print(depth, "z--", fpath.name)
            with ZipFile(fpath, 'r') as zf:
                for chunkfname in zf.filelist:
                    chunkfpath = Path(chunkfname.filename)
                    if chunkfpath.suffix == ".xml":
                        xmlstr = zf.read(chunkfname)
                        print(depth, "--z", chunkfpath.name)
                        cwd = Path(cwd).joinpath(fpath.parent)
                        xml = ET.fromstring(xmlstr)
                        # xmlprettyprint(xml)
                        parse_xml(cwd, xml, project_name)
                    else:
                        print(depth, "FILE IN ZIP", chunkfpath)
                        print()
        else:
            print(depth, "FILE", fpath)
            print()

    for child in root:
        parse_xml(cwd, child, project_name)


def parse_xmlfile(cwd, fname=None, project_name=None):
    warnings.warn("`parse_xmlfile` is a provisional function and may not exist in future versions.")

    # print out a psx project
    import xml.etree.ElementTree as ET
    if not fname:
        project_name = Path(cwd).stem
        fname = cwd
        cwd = Path(cwd).parent.as_posix()
    print("---", Path(fname).name)
    tree = ET.parse(fname)
    root = tree.getroot()
    parse_xml(cwd, root, project_name)


def copy_cameras_to_chunk(project: Project, from_chunk_id, to_chunk_id, camera_ids=[]):
    """
    Utility to copy images to other chunks, along with their masks.

    Useful for when you have "static" images you know are good and can work across multiple chunks
    """
    # add to chunk.cameras
    # add to frame.cameras
    # add to thumbnails
    # add to sensors
    # add to masks
    warnings.warn("`copy_cameras_to_chunk` is definitely a provisional function and will not exist in future versions.")

    from_chunk = project.apps[0].documents[0].chunks[from_chunk_id]
    from_frame = from_chunk.frames[0]

    to_chunk = project.apps[0].documents[0].chunks[to_chunk_id]
    to_frame = to_chunk.frames[0]

    for camera_id in camera_ids:
        new_id = len(to_chunk.cameras)
        # copy the chunk details
        chunkCamera = None
        for cc in from_chunk.cameras:
            if cc.id == camera_id:
                chunkCamera = cc
                break

        if not chunkCamera:
            warnings.warn(f"Unable to find {camera_id} in chunk cameras")
            return
        nc = copy.deepcopy(chunkCamera)
        nc.id = new_id
        to_chunk.cameras.append(nc)

        # copy the sensor details

        # copy the frame details
        frameCamera = None
        for fc in from_frame.cameras:
            if fc.camera_id == camera_id:
                frameCamera = fc
                break

        if not frameCamera:
            warnings.warn(f"Unable to find {camera_id} in frame cameras")
            return
        nc = copy.deepcopy(frameCamera)
        nc.camera_id = new_id
        to_frame.cameras.append(nc)

        # copy thumbnail details

        # check for a mask
        try:
            index = from_frame.masks.camera_ids.index(camera_id)
        except ValueError:
            continue
        # there is a mask, so add it to the new chunk too.
        if not to_frame.masks:
            to_frame.masks = Masks(version=__version_psx__)
            to_frame.masks._mask_data = {}
        if camera_id in from_frame.masks.camera_ids:
            to_frame.masks.camera_ids.append(new_id)
            mask_path = from_frame.masks.mask_paths[index]
            to_frame.masks.mask_paths.append(mask_path)
            data = copy.copy(from_frame.masks._mask_data[mask_path])
            to_frame.masks._mask_data[mask_path] = data
        print("finished copy for ", camera_id, " as ", new_id)


def duplicate_chunk(project: Project, chunk_id: int, number_of_repeats:int=1):
    """ Copy a chunk and add it to the end of the document """
    chunk = project.document.chunks[chunk_id]
    for i in range(number_of_repeats):
        new_chunk = copy.deepcopy(chunk)
        project.document.chunks.append(new_chunk)


def replace_chunk_photos(project: Project, chunk_id: int, new_photos: list):
    """ Replace the file paths for a photos in a chunk (good for switching textures on a model) """
    """ WORK IN PROGRESS"""
    chunk = project.document.chunks[chunk_id]
    if len(chunk.frames) > 1:
        warnings.warn(f"replace chunk only works on a single frame "
                      "Please open an issue at https://gitlab.com/dodgyville/pypsxlib/issues")

    # XXX: does not take into account relative paths.
    # XXX: This must be fixed.
    for frames in chunk.frames:
        for index, camera in enumerate(frames.cameras):
            camera.photo.path = new_photos[index]
