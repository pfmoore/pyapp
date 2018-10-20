from pyapp import main
from click.testing import CliRunner

def test_app_runs():
    """Confirm that we can run the application"""
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
