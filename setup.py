import cx_Freeze

executables = [cx_Freeze.Executable(
	script="a_void.py",
	icon="a_void.ico")]

cx_Freeze.setup(
    name="A VOID",
    version="2.0",
    author="avan",
    description="hatdog",
    options={"build_exe": {"packages":["pygame", "json"],
                           "include_files":["good_times_rg.ttf", "a_void_data.json", "odyssey.ogg"]}},
    executables = executables
    )
