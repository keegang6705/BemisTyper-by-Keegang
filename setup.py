from cx_Freeze import setup, Executable

setup(
    name="BemisTyper By Keegang",
    version="1.0",
    description="Bemis auto-typer",
    executables=[Executable("BemisTyper.py")],
)
