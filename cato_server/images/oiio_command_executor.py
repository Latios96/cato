import logging
import subprocess

logger = logging.getLogger(__name__)


class OiioCommandExecutor:
    def execute_command(self, command: str) -> str:
        logger.debug("Running command %s", command)
        status, output = subprocess.getstatusoutput(command)
        self._handle_command_error(command, status, output)
        return output

    def _handle_command_error(self, command, status, output):
        logger.debug(output)
        if not output.startswith("iinfo ERROR") and not output.startswith(
            "oiiotool ERROR"
        ):
            return
        is_not_an_image = any(
            message in output
            for message in [
                "OpenImageIO could not find a format reader",
                "Not a PNG file",
                "Empty file",
                "is not an OpenEXR file",
                "Cannot read TIFF header",
            ]
        )

        if is_not_an_image:
            raise NotAnImageException(output)

        if status == 0:
            return

        raise Exception(
            f"Exit code f{status} when running command {command}: output was: {output}"
        )


class NotAnImageException(Exception):
    def __init__(self, output):
        super(NotAnImageException, self).__init__(f"The file is not an Image! {output}")
