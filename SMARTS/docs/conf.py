                                                          
 
                                                                            
                             
                                                               

                                                                              

                                                                               
                                                                             
                                                                               
 
import os
import sys
from smarts import VERSION

sys.path.insert(0, os.path.abspath(".."))


                                                                              

project = "SMARTS"
copyright = "2021, Huawei Technologies."
author = "Huawei Noah's Ark Lab."

                                                
release = VERSION


                                                                              

                                                                     
                                                                     
       
extensions = [
    "myst_parser",                                        
    "sphinx.ext.autodoc",                                              
    "sphinx.ext.coverage",                                              
    "sphinx.ext.extlinks",                          
    "sphinx.ext.napoleon",                                      
    "sphinx.ext.todo",                          
    "sphinx.ext.viewcode",                                
    "sphinx_rtd_theme",                       
    "sphinx_click",                                                    
    "sphinxcontrib.apidoc",                                  
    "sphinxcontrib.spelling",                                    
]

extlinks = {
    "assets": (
        "https://github.com/huawei-noah/SMARTS/tree/master/smarts/assets/%s",
        "%s",
    ),
    "examples": (
        "https://github.com/huawei-noah/SMARTS/tree/master/examples/%s",
        "%s",
    ),
    "scenarios": (
        "https://github.com/huawei-noah/SMARTS/tree/master/scenarios/%s",
        "%s",
    ),
}
                                                        
                                               
apidoc_module_dir = ".."
apidoc_module_first = True
apidoc_excluded_paths = [
    "cli",
    "examples",
    "setup.py",
    "scenarios",
    "smarts/ros",
    "zoo/policies/interaction_aware_motion_prediction",
    "smarts/waymo/waymo_open_dataset/protos",
    "zoo/evaluation/metrics",
]
apidoc_extra_args = [
    "--force",
    "--separate",
    "--ext-viewcode",
    "--doc-project=SMARTS",
    "--maxdepth=2",
    "--templatedir=_templates/apidoc",
]
autodoc_mock_imports = [
    "av2",
    "cpuinfo",
    "cv2",
    "gymnasium",
    "lxml",
    "mdutils",
    "moviepy",
    "opendrive2lanelet",
    "pandas",
    "pathos",
    "PIL",
    "pynput",
    "ray",
    "rich",
    "tabulate",
    "tools",
    "torch",
]

todo_include_todos = True

                                                                        
templates_path = ["_templates"]

                                                                      
                                                      
                                                                 
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

                                                                                   

nitpick_ignore = {
    ("py:class", "optional"),
    ("py:class", "ellipsis"),
    ("py:class", "function"),
                                                                      
                                                                           
    ("py:class", "Score"),
    ("py:class", "Done"),
    ("py:class", "CostFuncs"),
    ("py:class", "ActType"),
    ("py:class", "ObsType"),
    ("py:class", "smarts.env.gymnasium.wrappers.metric.utils.T"),
    ("py:class", "enum.Enum"),
    ("py:class", "bc.BulletClient"),
}
nitpick_ignore_regex = {
    (r"py:.*", r"av2\..*"),
    (r"py:.*", r"google\.protobuf\..*"),
    (r"py:.*", r"grpc\..*"),
    (r"py:.*", r"gym\..*"),
    (r"py:.*", r"gymnasium\..*"),
    (r"py:.*", r"logging\..*"),
    (r"py:.*", r"multiprocessing\..*"),
    (r"py:.*", r"np\..*"),
    (r"py:.*", r"numpy\..*"),
    (r"py:.*", r"opendrive2lanelet\..*"),
    (r"py:.*", r"panda3d\..*"),
    (r"py:.*", r"pathlib\..*"),
    (r"py:.*", r"pybullet(_utils)?\..*"),
    (r"py:.*", r"re\..*"),
    (r"py:.*", r"shapely\..*"),
    (r"py:.*", r"sumo(lib)?\..*"),
    (r"py:.*", r"tornado\..*"),
    (r"py:.*", r"traci\..*"),
    (r"py:.*", r"typing(_extensions)?\..*"),
    (r"py:.*", r"configparser\..*"),
    (r"py:class", r".*\.?T"),
    (r"py:class", r".*\.?S"),
}

                                                                              
linkcheck_anchors = False
linkcheck_ignore = [
    r"https?://localhost:\d+/?",
    r"https?://ops.fhwa.dot.gov.*",                                                                  
]
linkcheck_retries = 2

                                                                              
spelling_exclude_patterns = ["ignored_*", "**/*_pb2*"]
spelling_ignore_pypi_package_names = True
spelling_show_suggestions = True
spelling_suggestion_limit = 2
spelling_ignore_contributor_names = False
spelling_word_list_filename = ["spelling_wordlist.txt"]

                                                                              

                                                                           
                           
 
                          
html_theme = "sphinx_rtd_theme"

                                                                             
                                                                             
                                                                         
html_static_path = ["_static"]
