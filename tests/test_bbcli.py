from typer.testing import CliRunner

from bbcli import __app_name__, __version__, cli, getuser, getcoursecontents

runner = CliRunner()

def test_version():
	# invokes the command line and checks the version
	result = runner.invoke(cli.app, ["--version"])
	assert result.exit_code == 0

	assert result.output == f"{__app_name__} v{__version__}\n"
	#assert f"{__app_name__} v{__version__}\n" in result.stdout

def test_endpoint_getuser():
	result = runner.invoke(getuser, input='hanswf')
	assert not result.exception 

def test_endpoint_getcoursecontents():
	res = runner.invoke(getcoursecontents)
	assert not res.exception