import cx_Freeze

executables = [cx_Freeze.Executable("stinkyquest.py")]

cx_Freeze.setup(
    name="StinkyQuest",
    options={"build_exe": {"packages":["pygame", "time", "random", "sys"],
                           "include_files":["data/bella.png", "data/biscuits.png", "data/stinky.png", "data/freesansbold.ttf"]}},
    executables = executables

    )
