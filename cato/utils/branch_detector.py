import subprocess
from typing import Optional

from cato_common.utils.change_cwd import change_cwd


class BranchDetector:
    def detect_branch(self, folder) -> Optional[str]:
        with change_cwd(folder):
            status, output = subprocess.getstatusoutput(
                "git rev-parse --is-inside-work-tree"
            )
            if status != 0 or not output.startswith("true"):
                return None
            status, output = subprocess.getstatusoutput(
                "git rev-parse --abbrev-ref HEAD"
            )
            if status != 0:
                return None
            return output
