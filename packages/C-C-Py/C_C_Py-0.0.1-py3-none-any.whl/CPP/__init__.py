try:
    f = open('settings.h','r')
except Exception:
    f = open('settings.h','w')
    f.write('C:0')
    f.close()
for line in f:
    #print(line)
    if line.startswith('C:') and line.endswith('0'):
        
        try:
            from CPP import _for
            print('impoting cpp.for')
        except Exception as e:
             print('warning cpp.for could not be imported! reason: ' + str(e))
def package_vector():
    try:
        from CPP import vector
    except Exception as e:
        print(e)
def package_speech():
    try:
        from CPP import speech
    except Exception as e:
        print(e)
def package_binary():
    try:
        from CPP import binary_lib
    except Exception as e:
        print(e)

f.close()
del f
def SHUTDOWN_SOURCE():
    quit()
def SHUTDOWN_SCRIPT():
    exit()
