import json
import os
import shutil
import uuid
from typing import Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape
from oiio.OpenImageIO import ImageBuf


class HtmlReporter:

    def report(self, results: Dict, path: str):

        for suite_result in results['result']:
            for test_result in suite_result['test_results']:
                test_result['copied_image'] = self._copy_image(path, test_result['image_output'])

        with open(os.path.join(path, 'index.html'), "w") as f:
            f.write(self._render_template(results))

        self._copy_static_resources(path)

    def _render_template(self, data):
        env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template('index.html')
        return template.render(data)

    def _copy_image(self, path, image_path):
        image_path = os.path.abspath(image_path)
        path = os.path.abspath(path)
        folder = os.path.join(path, 'images')
        target_path = os.path.join(folder, f"{uuid.uuid4()}{os.path.splitext(image_path)[1]}")
        if not os.path.exists(folder):
            os.makedirs(folder)

        return self._copy_or_convert(image_path, target_path)

    def _copy_or_convert(self, image_path, target_path):
        print(image_path)
        if os.path.splitext(image_path)[1].lower() in ['.png', '.jpg', 'jpeg']:
            shutil.copy(image_path, target_path)
        else:
            target_path = os.path.splitext(target_path)[0] + ".png"

            buf = ImageBuf(image_path)
            buf.write(target_path)

        return target_path

    def _copy_static_resources(self, path):
        static_resources = self._resolve_resources([
            'termynal.js',
            'termynal.css',
        ])

        for resource in static_resources:
            target_path = os.path.join(path, os.path.basename(resource))
            shutil.copy(resource, target_path)

    def _resolve_resources(self, resources):
        res = []
        for r in resources:
            res.append(os.path.join(os.path.dirname(__file__), 'templates', r))
        return res


if __name__ == '__main__':
    with open(r'M:\test\cato-arnold_suite\report.json') as f:
        data = json.load(f)

        report = HtmlReporter()
        report.report(data, r'M:\test\cato-arnold_suite\report')
