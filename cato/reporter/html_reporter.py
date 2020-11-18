import logging
import copy
import json
import os
import shutil
from typing import Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape
from oiio.OpenImageIO import ImageBuf, ImageBufAlgo

logger = logging.getLogger(__name__)


class HtmlReporter:
    def report(self, results: Dict, path: str):

        for suite_result in results["result"]:
            for test_result in suite_result["test_results"]:
                test_result["copied_image"] = self._copy_image(
                    path, test_result["image_output"]
                )

        failed_tests = self._filter_results(results, "TestStatus.FAILED")["result"]
        results["has_failed_tests"] = bool(failed_tests)
        results["failed_tests"] = failed_tests
        results["succeded_tests"] = self._filter_results(results, "TestStatus.SUCCESS")[
            "result"
        ]

        with open(os.path.join(path, "index.html"), "w") as f:
            logger.info("Rendering template..")
            f.write(self._render_template(results))

        self._copy_static_resources(path)

    def _render_template(self, data):
        env = Environment(
            loader=FileSystemLoader(
                os.path.join(os.path.dirname(__file__), "templates")
            ),
            autoescape=select_autoescape(["html", "xml"]),
        )
        template = env.get_template("index.html")
        return template.render(data)

    def _copy_image(self, path, image_path):
        image_path = os.path.abspath(image_path)
        path = os.path.abspath(path)
        folder = os.path.join(path, "images")
        checksum = self._checksum(image_path)
        target_path = os.path.join(
            folder, f"{checksum}{os.path.splitext(image_path)[1]}"
        )
        if not os.path.exists(target_path):
            if not os.path.exists(folder):
                os.makedirs(folder)

            return self._copy_or_convert(image_path, target_path)

    def _copy_or_convert(self, image_path, target_path):
        if os.path.splitext(image_path)[1].lower() in [".png", ".jpg", "jpeg"]:
            logger.info("Copy image %s", image_path)
            shutil.copy(image_path, target_path)
        else:
            logger.info("Converting image %s to png", image_path)
            target_path = os.path.splitext(target_path)[0] + ".png"

            buf = ImageBuf(image_path)
            buf.write(target_path)

        return target_path

    def _copy_static_resources(self, path):
        logger.info("Copy static resources..")
        static_resources = self._resolve_resources(
            [
                "termynal.js",
                "termynal.css",
                "cato.css",
            ]
        )

        for resource in static_resources:
            target_path = os.path.join(path, os.path.basename(resource))
            shutil.copy(resource, target_path)

    def _resolve_resources(self, resources):
        res = []
        for r in resources:
            res.append(os.path.join(os.path.dirname(__file__), "templates", r))
        return res

    def _filter_results(self, results, test_status):
        results = copy.deepcopy(results)
        for suite_result in results["result"]:
            tests = []
            for test_result in suite_result["test_results"]:
                if test_result["result"] == test_status:
                    tests.append(test_result)
            suite_result["test_results"] = tests
        return results

    def _checksum(self, image_path: str) -> str:
        A = ImageBuf(image_path)
        return ImageBufAlgo.computePixelHashSHA1(A, blocksize=64)


if __name__ == "__main__":
    with open(r"M:\test\cato-arnold_suite\report.json") as f:
        data = json.load(f)

        report = HtmlReporter()
        report.report(data, r"M:\test\cato-arnold_suite\report")
