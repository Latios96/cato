import subprocess

from cato.utils.branch_detector import BranchDetector
from cato_common.utils.change_cwd import change_cwd


def test_should_return_none_if_not_in_a_git_repo(tmp_path):
    branch_detector = BranchDetector()

    branch = branch_detector.detect_branch(str(tmp_path))

    assert branch is None


def test_should_branch_name(tmp_path):
    branch_detector = BranchDetector()
    with change_cwd(str(tmp_path)):
        subprocess.check_output(["git", "init"])
        (tmp_path / "test.txt").touch()
        subprocess.check_output(["git", "add", "test.txt"])
        subprocess.check_output(["git", "config", "user.name", "Foo Bar"])
        subprocess.check_output(["git", "config", "user.email", "foo.bar@bar.com"])
        subprocess.check_output(["git", "commit", "-m", "test"])

    branch = branch_detector.detect_branch(str(tmp_path))

    assert branch.startswith("m")
