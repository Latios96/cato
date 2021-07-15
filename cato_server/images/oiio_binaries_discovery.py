import subprocess


class OiioBinariesDiscovery:
    def get_iiinfo_executable(self) -> str:
        return "iinfo"

    def get_oiiotool_executable(self) -> str:
        return "oiiotool"

    def binaries_are_available(self) -> bool:
        return self._is_available(self.get_iiinfo_executable()) and self._is_available(
            self.get_oiiotool_executable()
        )

    def _is_available(self, binary: str) -> bool:
        status, output = subprocess.getstatusoutput(f"{binary} -help")
        return status == 0
