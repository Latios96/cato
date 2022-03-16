from pathlib import Path

from py_typescript_generator import TypeGenerationPipelineBuilder

from cato_common.domain.can_be_edited import CanBeEdited
from cato_common.domain.project import Project

if __name__ == "__main__":
    TypeGenerationPipelineBuilder().for_types([Project, CanBeEdited]).to_file(
        Path(__file__).parent.parent
        / "frontend"
        / "src"
        / "catoapimodels"
        / "catoapimodels.ts"
    ).build().run()
