import os
import time
import sys
import subprocess

buildroot = os.getcwd()

os.chdir('source')
os.chdir('anuga')


print 'Changing to', os.getcwd()        

#entries = listdir('.')

t0 = time.time()

# Attempt to compile all ANUGA extensions

execfile('compile_all.py')

#os.chdir('utilities')
#subprocess.call([sys.executable, 'compile.py', 'quad_tree.c'])
#subprocess.call([sys.executable, 'compile.py', 'sparse_dok.c'])
#subprocess.call([sys.executable, 'compile.py', 'sparse_csr.c'])
#execfile('compile_all.py')
#
#os.chdir('..')
#os.chdir('advection')
#execfile('..' + os.sep + 'utilities' + os.sep + 'compile.py')
#
#os.chdir('..')
#os.chdir('operators')
#execfile('..' + os.sep + 'utilities' + os.sep + 'compile.py')
#
#os.chdir('..')
#os.chdir('file_conversion')
#execfile('..' + os.sep + 'utilities' + os.sep + 'compile.py')
#
#os.chdir('..')
#os.chdir('geometry')
#execfile('..' + os.sep + 'utilities' + os.sep + 'compile.py')
#
#os.chdir('..')
#os.chdir('structures')
#execfile('..' + os.sep + 'utilities' + os.sep + 'compile.py')
#
#os.chdir('..')
#os.chdir('abstract_2d_finite_volumes')
#execfile('..' + os.sep + 'utilities' + os.sep + 'compile.py')
#
#os.chdir('..')
#os.chdir('file')
#execfile('..' + os.sep + 'utilities' + os.sep + 'compile.py')
#
#os.chdir('..')
#os.chdir('shallow_water')
#execfile('..' + os.sep + 'utilities' + os.sep + 'compile.py')
#
#
#os.chdir('..')
#os.chdir('mesh_engine')
#execfile('..' + os.sep + 'utilities' + os.sep + 'compile.py')
#
#os.chdir('..')
#os.chdir('fit_interpolate')
#subprocess.call([sys.executable, '..' + os.sep + 'utilities' + os.sep + 'compile.py', 'rand48.c'])
#subprocess.call([sys.executable, '..' + os.sep + 'utilities' + os.sep + 'compile.py', 'ptinpoly.c'])
#execfile('..' + os.sep + 'utilities' + os.sep + 'compile.py')


os.chdir(buildroot)    

try:
    print '-----------------------------------------------'
    print 'Attempting to compile Metis for parallel ANUGA!'
    print '-----------------------------------------------'

    import pypar

    # Attempt to compile Metis for use with anuga_parallel
    os.chdir('source')
    os.chdir('anuga_parallel')
    os.chdir('pymetis')

    make_logfile = os.path.join(buildroot, 'make_metis.log')
    options = ''
    if sys.platform == 'win32':
        options = 'for_win32'
    else:
        if os.name == 'posix':
            if os.uname()[4] in ['x86_64', 'ia64']:
                options = ' '

    make_command = 'make %s > %s' % (options, make_logfile)
    print make_command
    err = os.system(make_command)
    if err != 0:
        msg = 'Could not compile Metis '
        msg += 'on platform %s, %s\n' % (sys.platform, os.name)
        msg += 'You need to compile Metis manually '
        msg += 'if you want to run ANUGA in parallel.'
        raise Exception, msg
    else:
        msg = 'Compiled Metis succesfully. Output from Make is available in %s'\
            % make_logfile
        print msg

    print 
    print '-----------------------------------------------'
    print 'Attempting to compile pypar_extras'
    print '-----------------------------------------------'

    os.chdir('..')
    os.chdir('pypar_extras')

    cmd = 'python anuga_setup.py'
    print cmd
    err = os.system(cmd)
    if err != 0:
        msg = 'Could not compile pypar_extras '
        msg += 'on platform %s, %s\n' % (sys.platform, os.name)
        msg += 'You need to compile pypar_extras manually '
        msg += 'if you want to run ANUGA in parallel.'
        raise Exception, msg
    else:
        msg = 'Compiled pypar_extras succesfully.'
        print msg
except:
    print 'anuga_parallel code not compiled as pypar not installed'



print        
print 'That took %.3fs' %(time.time() - t0)




