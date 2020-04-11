#!/usr/bin/env python
"""Run a test calculation on localhost.

Usage: ./example_01.py
"""
import os
from package_template import tests, helpers
from aiida import cmdline, engine
from aiida.plugins import DataFactory, CalculationFactory
import click


def test_run(package_template_code):
    """Run a calculation on the localhost computer.

    Uses test helpers to create AiiDA Code on the fly.
    """
    if not package_template_code:
        # get code
        computer = helpers.get_computer()
        package_template_code = helpers.get_code(
            entry_point='package_template', computer=computer)

    # Prepare input parameters
    DiffParameters = DataFactory('package_template')
    parameters = DiffParameters({'ignore-case': True})

    SinglefileData = DataFactory('singlefile')
    file1 = SinglefileData(
        file=os.path.join(tests.TEST_DIR, "input_files", 'file1.txt'))
    file2 = SinglefileData(
        file=os.path.join(tests.TEST_DIR, "input_files", 'file2.txt'))

    # set up calculation
    inputs = {
        'code': package_template_code,
        'parameters': parameters,
        'file1': file1,
        'file2': file2,
        'metadata': {
            'description':
            "Test job submission with the package_template plugin",
        },
    }

    # Note: in order to submit your calculation to the aiida daemon, do:
    # from aiida.engine import submit
    # future = submit(CalculationFactory('package_template'), **inputs)
    result = engine.run(CalculationFactory('package_template'), **inputs)

    computed_diff = result['package_template'].get_content()
    print("Computed diff between files: \n{}".format(computed_diff))


@click.command()
@cmdline.utils.decorators.with_dbenv()
@cmdline.params.options.CODE()
def cli(code):
    """Run example.

    Example usage: $ ./example_01.py --code diff@localhost

    Alternative (creates diff@localhost-test code): $ ./example_01.py

    Help: $ ./example_01.py --help
    """
    test_run(code)


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
