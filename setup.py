from cx_Freeze import setup, Executable



setup(name = 'osuanimation', 
      version='3', 
      description='I love it',
      executables = [Executable(script='Display.py', base='Win32GUI')])
