'''
  PyInstaller specification for TRTA 
  Leon S. Kim

  Description:
    If "onefile" is True(default), a single executable file will be created. 
    Otherwise(onedir), an excutable file and the other files(libraries, resources)
    will be create in a directory.
'''

# -*- mode: python -*-

###############
# Output Type #
###############

onefile = True


#######################
# DO NOT MODIFY BELOW #
#######################

resources = [
              (os.path.join('qml', 'TRTA.qml'), os.path.join('qml', 'TRTA.qml'), 'DATA'),
              (os.path.join('qml', 'Button.qml'), os.path.join('qml', 'Button.qml'), 'DATA'),
              (os.path.join('qml', 'Progress.qml'), os.path.join('qml', 'Progress.qml'), 'DATA'),
              (os.path.join('qml', 'Notification.qml'), os.path.join('qml', 'Notification.qml'), 'DATA'),
              (os.path.join('qml', 'Speaker.qml'), os.path.join('qml', 'Speaker.qml'), 'DATA'),
              (os.path.join('images', 'tomato.png'), os.path.join('images', 'tomato.png'), 'DATA'),
              (os.path.join('images', 'gauge.png'), os.path.join('images', 'gauge.png'), 'DATA'),
              (os.path.join('images', 'phase_ready.png'), os.path.join('images', 'phase_ready.png'), 'DATA'),
              (os.path.join('images', 'phase_work.png'), os.path.join('images', 'phase_work.png'), 'DATA'),
              (os.path.join('images', 'phase_break.png'), os.path.join('images', 'phase_break.png'), 'DATA'),
              (os.path.join('images', 'phase_long_break.png'), os.path.join('images', 'phase_long_break.png'), 'DATA'),
              (os.path.join('images', 'sound_on.png'), os.path.join('images', 'sound_on.png'), 'DATA'),
              (os.path.join('images', 'sound_off.png'), os.path.join('images', 'sound_off.png'), 'DATA'),
              (os.path.join('wav', 'notify.wav'), os.path.join('wav', 'notify.wav'), 'DATA')
             ]

a = Analysis(['TRTA.py'],
             pathex=[],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)


if onefile:
  exe = EXE(pyz,
            Tree('qml', prefix='qml'),
            Tree('images', prefix='images'),
            Tree('wav', prefix='wav'),
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            resources,
            name='TRTA.exe',
            debug=False,
            strip=None,
            upx=True,
            console=False)
else:
  exe = EXE(pyz,
              a.scripts,
              exclude_binaries=True,
              name='TRTA.exe',
              debug=False,
              strip=None,
              upx=True,
              console=False)
  coll = COLLECT(exe,
                   a.binaries,
                   a.zipfiles,
                   a.datas,
                   resources,
                   strip=None,
                   upx=True,
                   name='TRTA')