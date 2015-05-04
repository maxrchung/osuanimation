from cx_Freeze import setup, Executable



setup(name = 'osuanimation', 
      version='1', 
      description='',
      executables = [Executable(script='Display.py'])
