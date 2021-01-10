from cx_Freeze import setup, Executable

executables = [Executable('main.py',
                          targetName='Super_Mario.exe',
                          base='Win32GUI',
                          icon='icon.ico')]

includes = ['pygame', 'pygame_menu', 'os']

zip_include_packages = ['pygame', 'pygame_menu', 'os']

include_files = ['Player.py', 'Platforms.py', 'Variables.py', 'Interface.py', 'init_var.txt',
                 'gamer.txt', 'Defs.py', 'data.py', 'sound_data/batman.mp3',
                 'sound_data/checkpoint_loaded_sound.mp3', 'sound_data/dead_sound.mp3',
                 'sound_data/Exit_sound.mp3', 'sound_data/get_money_sound.mp3',
                 'sound_data/hit_sound.mp3', 'sound_data/jump_sound.mp3',
                 'sound_data/open_sound.mp3', 'sound_data/pause_btn_sound.mp3',1
                 'sound_data/play btn sound.mp3', 'sound_data/Race to Mars.mp3',
                 'sound_data/win_sound.mp3', 'level_data/level_1.txt', 'level_data/level_2.txt',
                 'level_data/sandbox.txt', '']

options = {
    'build_exe': {
        'include_msvcr': True,
        'includes': includes,
        'zip_include_packages': zip_include_packages,
        'build_exe': 'build_windows',
        'include_files': include_files,
    }
}

setup(name=' main',
      version='0.0.3',
      description='My app',
      executables=executables,
      options=options)
