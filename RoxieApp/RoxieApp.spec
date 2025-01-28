# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

# Analysis of the Python script
a = Analysis(
    ['qt_output.py'],  # Replace with the name of your Python script
    pathex=['/home/paul/Desktop/Roxie-Sales/qt_exe'],  # Set the path to your project directory (where qt_output.py is located)
    binaries=[],  # Add any binaries if required (empty list if not needed)
    datas=[
        ('qt_assets/*', 'qt_assets'),  # Include all files from the qt_assets directory (for images, sounds, etc.)
        ('.env', '.'),  # Include .env file in the root of the app (for environment variables)
        ('assets/*', 'assets'),
        ('company_specific_info.txt', '.')
        # Add more assets or files if needed
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# PyZ archive creation (bundles your pure Python code)
pyz = PYZ(a.pure)

# Create the executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='RoxieApp',  # Output executable name
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Enable UPX compression
    upx_exclude=[],  # Exclude specific files from UPX compression if needed
    runtime_tmpdir=None,
    console=False,  # Set to False for a windowed app (no terminal)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
