#!/usr/bin/python

# Produce documentation.
# Run this from the root directory.
# This picks up properties from ../documentation_configuration.py.
# Documentation source files for various projects (that are indicated in
# documentation_configuration.py) should be in ./PROJECT/doc.

import sys

sys.path.insert (1, '.')
import documentation_configuration

import os, errno, subprocess, shutil

##### Set up paths and file names.

targetPath = documentation_configuration.targetPath
targetSourcePath = os.path.join (targetPath, 'source')
doxygenOutputPath = os.path.join (targetPath, 'doxygen')
sphinxOutputPath = os.path.join (targetPath, 'html')

# The Doxygen configuration file is called "Doxyfile".
doxyFileName = os.path.join (targetSourcePath, 'Doxyfile')

sphinxMainFileName = os.path.join (targetSourcePath, 'index.rst')
sphinxConfigurationFileName = os.path.join (targetSourcePath, 'conf.py')

sourceSphinxConfigurationFileName = 'doc/sphinx-conf.py'

mainProject = documentation_configuration.mainProject
mainProjectName = documentation_configuration.mainProjectName

def projectDocumentationSource (project):
    ''':return: the source for documentation for project ``project``.'''
    # Expect documentation in ./PROJECT/doc.
    return os.path.join (project, 'doc')

subProjects = [project for project in documentation_configuration.subProjects
    if os.path.exists (projectDocumentationSource (project))]
allProjects = [mainProject] + subProjects

##### File handling

def generateFile (name, commentPattern = ('# ', '# ')):
    '''
    Open a writeable text file that starts with a warning that it has been
    automatically generated.
    '''
    f = open (name, 'w')
    f.write ('%sThis file has been generated automatically '
            'by build_documentation.py.\n'
        '%sTherefore, you probably do not want to edit this file by hand.\n\n'
        % commentPattern)
    return f

def makeDir (path):
    '''Create a directory but do not mind if it exists.'''
    try:
        os.makedirs (path)
    except OSError, e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise

def makeSymbolicLink (source, target):
    '''Create a symbolic link but do not mind if it exists.'''
    try:
        os.symlink (os.path.relpath (source, os.path.dirname (target)), target)
    except OSError, e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise

##### Generate Doxygen configuration file.

def generateDoxygen():

    makeDir (doxygenOutputPath)

    print '**** Building Doxygen documentation.'

    doxyFile = generateFile (doxyFileName)

    doxyFile.write ('PROJECT_NAME = "%s"\n'
        % documentation_configuration.mainProjectName)
    doxyFile.write ('OUTPUT_DIRECTORY = "%s"\n' % doxygenOutputPath)

    doxyFile.write ('\n# Use files from projects: %s\n'
        % ", ".join (allProjects))

    sourcePaths = ['%s/include' % project for project in allProjects]
    sourcePathList = ' '.join (sourcePaths)

    doxyFile.write ('INPUT = %s\n' % sourcePathList)
    doxyFile.write ('RECURSIVE = YES\n')

    doxyFile.write ('STRIP_FROM_PATH = %s\n' % sourcePathList)
    doxyFile.write ('STRIP_FROM_INC_PATH = %s\n' % sourcePathList)

    doxyFile.write ('\n'
        'GENERATE_HTML          = YES\n'
        'HTML_OUTPUT            = html\n'
        '\n'
        'GENERATE_XML           = YES\n'
        'XML_OUTPUT             = xml\n'
        '\n'
        'GENERATE_LATEX         = NO\n')


    doxyFile.write ('GENERATE_TAGFILE = %s/tag\n' % doxygenOutputPath)

    doxyFile.write ('\n'
        'EXTRACT_ALL            = YES\n'
        'EXTRACT_STATIC         = YES\n'
        'HIDE_UNDOC_MEMBERS     = NO\n'
        '\n'
        '\nSOURCE_BROWSER         = NO\n'
        'STRIP_CODE_COMMENTS    = YES\n'
        '\n'
        '\nENABLE_PREPROCESSING   = YES\n'
        'MACRO_EXPANSION        = YES\n'
        'EXPAND_ONLY_PREDEF     = YES\n'
        'PREDEFINED             = DOXYGEN_SKIP_THIS "RETURNS(argument)= {}"\n'
        '\n'
        '\nGENERATE_TODOLIST = YES\n'
        'QUIET = YES\n')

    doxyFile.close()

##### Generate Sphinx configuration file.

def generateSphinx():
    print '**** Building Sphinx documentation.'

    for project in allProjects:
        makeSymbolicLink (projectDocumentationSource (project),
            os.path.join (targetSourcePath, project))

    sphinxMainFile = generateFile (sphinxMainFileName, ('..  ', '    '))

    sphinxMainFile.write (
        '..  The conventions for the headings are the same '
            'as the Python documentation:\n'
        '\n'
        '    # with overline, for parts\n'
        '    * with overline, for chapters\n'
        '    =, for sections\n'
        '    -, for subsections\n'
        '    ^, for subsubsections\n'
        '    ", for paragraphs\n'
        '\n')

    mainProjectHeaderLine = len (mainProjectName) * '#'

    sphinxMainFile.write ((3 * '%s\n') %
        (mainProjectHeaderLine, mainProjectName, mainProjectHeaderLine))

    sphinxMainFile.write ('\n'
        'This project contains a number of sub-projects.\n'
        'The documentation for the main project is:\n'
        '\n'
        'Contents:\n'
        '\n'
        '.. toctree::\n'
        '    :maxdepth: 2\n'
        '\n'
        '    %s/index\n'
        '\n' % mainProject)

    if subProjects != []:
        sphinxMainFile.write (
            '############\n'
            'Dependencies\n'
            '############\n'
            '\n'
            'This project depends on the folling sub-projects:\n'
            '\n'
            '.. toctree::\n'
            '    :maxdepth: 2\n'
            '\n')
        for project in subProjects:
            sphinxMainFile.write ('    %s/index\n' % project)

    sphinxMainFile.write (
        '\n'
        '##################\n'
        'Indices and tables\n'
        '##################\n'
        '\n'
        '* :ref:`genindex`\n'
        '* :ref:`search`\n')

    sphinxMainFile.close()

    shutil.copyfile (sourceSphinxConfigurationFileName,
        sphinxConfigurationFileName)

    subprocess.check_call (['sphinx-build',
        '-b', 'html', targetSourcePath, sphinxOutputPath])

makeDir (targetPath)
makeDir (targetSourcePath)
generateDoxygen()
subprocess.check_call (['doxygen', doxyFileName])
generateSphinx()
