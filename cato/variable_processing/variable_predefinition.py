from dataclasses import dataclass
from typing import Dict


@dataclass
class VariablePredefinition:
    name: str
    variables: Dict[str, str]


MAYA_PREDEFINITION = VariablePredefinition(
    name="Autodesk Maya",
    variables={
        "maya_version": "2020",
        "maya_location": r"C:\Program Files\Autodesk\Maya{@maya_version}",
    },
)

VRAY_FOR_MAYA_PREDEFINITION = VariablePredefinition(
    name="V-Ray for Maya",
    variables={
        "vray_scene_file": "{@test_resources}/scene.vrscene",
        "vray_render_command": r'"{@maya_location}\vray\bin\vray.exe" -sceneFile={@vray_scene_file} -imgFile={@image_output_exr} -progressIncrement=1',
        "vray_gpu_render_command": r'"{@maya_location}\vray\bin\vray.exe" -sceneFile={@vray_scene_file} -imgFile={@image_output_exr} -progressIncrement=1 -rtengine=5',
    },
)

MTOA_PREDEFINITION = VariablePredefinition(
    name="Arnold for Maya",
    variables={
        "arnold_scene_file": "{@test_resources}/{@test_name}.ass",
        "arnold_location": r"C:\Program Files\Autodesk\Arnold\maya{@maya_version}",
        "arnold_render_command": r'"{@arnold_location}\bin\kick" -i {@test_resources}/{@test_name}.ass -o {@image_output_png} -of exr -dw -v 2',
    },
)

BLENDER_PREDEFINITION = VariablePredefinition(
    name="Blender",
    variables={
        "blender_scene_file": "{@test_resources}/{@test_name}.blend",
        "blender_version": "2.90",
        "blender_location": r"C:\Program Files\Blender Foundation\Blender {@blender_version}",
        "blender_render_command": r'"{@blender_location}\blender.exe" -b  {@blender_scene_file} -o {@image_output_folder}/{@test_name} -F PNG -f {@frame}',
    },
)

PREDEFINITIONS = [
    MAYA_PREDEFINITION,
    VRAY_FOR_MAYA_PREDEFINITION,
    MTOA_PREDEFINITION,
    BLENDER_PREDEFINITION,
]
