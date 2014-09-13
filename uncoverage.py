#!/usr/bin/env python
import os
import io
from coverage import coverage
import sys
from swampdragon.runtests import runtests


def qualify(data, report_file):
    if report_file and report_file not in data:
        return False
    percentage_line = data.split('%')[0]
    val = int(percentage_line[percentage_line.rfind(' '):])
    return val < 100


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = io.StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout


if __name__ == '__main__':
    # A rather hacky way to run coverage on a specific file
    report_file = None
    if len(sys.argv) > 1:
        report_file = sys.argv[-1]
        sys.argv = sys.argv[:-1]

    sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'swampdragon.runtests.settings'

    cov = coverage(source=['swampdragon'], omit=[
        './swampdragon/tests/*',
        'swampdragon/__init__.py',
        'swampdragon/core/__init__.py',
        'swampdragon/runtests/runtests.py',
        'swampdragon/runtests/settings.py',
        'swampdragon/swampdragon_server.py',
        'swampdragon/pubsub_providers/mock_publisher.py',
        'swampdragon/pubsub_providers/mock_sub_provider.py',
    ])
    cov.start()

    runtests.run_tests()

    cov.stop()
    cov.save()

    out = []
    with Capturing(out) as report:
        cov.report()

    output = [report[0]]
    for line in report:
        if '%' in line:
            if qualify(line, report_file):
                output.append(line)
    print('\n'.join(output))
