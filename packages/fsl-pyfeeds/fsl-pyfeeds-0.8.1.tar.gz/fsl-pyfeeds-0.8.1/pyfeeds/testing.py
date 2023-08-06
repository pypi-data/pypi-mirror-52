#!/usr/bin/env python
#
# testing.py - the testing module
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""The ``testing`` module contains the :class:`Test` class, which represents
a single pyfeeds test. It also contains the following functions:

.. autosummary::
   :nosignatures:

   findTestDirs
   listTests
   bundleTests
   runTests
   runTest
"""


from __future__ import print_function
from __future__ import division

import logging

import            os
import os.path as op
import            sys
import            time
import            shutil
import            hashlib
import            subprocess

from multiprocessing.pool import ThreadPool as Pool

from . import evaluate
from . import hashing
from . import common


log = logging.getLogger(__name__)


class Test(object):
    """The ``Test`` class represents a single pyfeeds test. A ``Test`` object
    has a few useful methods:


    .. autosummary::
       :nosignatures:

       hashInputs
       hashTestDir
       createSandbox


    The following attributes are available on a ``Test`` object:

    ============== ==========================================================
    ``name``       A unique, human readable, internal name for this ``Test``,
                   generated from the test directory path.

    ``testDir``    The test directory.

    ``testScript`` The full path to the ``feedsRun`` test executable.
    ============== ==========================================================
    """


    def __init__(self, testDir, baseDir):
        """Create a ``Test`` object.

        :arg testDir: The test directory.

        :arg baseDir: The *base* directory. This is identified by pyfeeds as
                      the parent directory of all tests which have been
                      specified by the user - see the
                      :func:`.nearestCommonAncestor` function.
        """

        if testDir == baseDir:
            self.name = op.basename(testDir)
        else:
            self.name = (testDir[len(baseDir):]
                         .replace(op.sep, '_')
                         .strip('_'))

        self.testDir    = op.abspath(testDir)
        self.baseDir    = op.abspath(baseDir)
        self.testScript = op.join(self.testDir, 'feedsRun')

        self.__inputs   = self.__loadInputsFile()

        if not op.isfile(self.testScript):
            raise RuntimeError('Test script {} does not '
                               'exist'.format(self.testScript))


    def __str__(self):
        """Returns a string representation of this ``Test``."""
        return self.name


    def __repr__(self):
        """Returns a string representation of this ``Test``."""
        return self.name


    def getInputs(self):
        """Return a list containing the paths to the external data
        dependencies of this ``Test``.
        """
        return list(self.__inputs)


    def inputsChangedSince(self, inputDir, mtime):
        """Returns ``True`` if any of the input files for this test
        have changed since the given ``datetime`` object.
        """
        inputs = [op.join(inputDir, i) for i in self.__inputs]
        return not all([common.allBefore(i, mtime) for i in inputs])


    def hashTestDir(self):
        """Calculates and returns MD5 digest of the contents of the test
        directory. See the :func:`.hashPath` method.
        """
        log.debug('Test {} - hashing test directory'.format(self.name))

        hashObj = hashlib.md5()
        count   = hashing.hashPath(self.testDir, hashObj)
        digest  = hashObj.hexdigest()

        log.debug('Test {} - test directory hash ({} files): {}'.format(
            self.name, count, digest))

        return digest


    def hashInputs(self, inputDir):
        """Calculates and returns MD5 digest of all external/shared data upon
        which this ``Test`` is dependent. See the :func:`.hashPath` method.

        :arg inputDir: Directory in which the test input data is located.
        """

        log.debug('Test {} - hashing inputs'.format(self.name))

        hashObj = hashlib.md5()

        count = 0
        for src in self.__inputs:
            src     = op.join(inputDir, src)
            count  += hashing.hashPath(src, hashObj)

        if count == 0: digest = None
        else:          digest = hashObj.hexdigest()

        log.debug('Test {} - input hash ({} files): {}'.format(
            self.name, count, digest))

        return digest


    def createSandbox(self, inputDir, sandbox=None, symlink=True):
        """Creates a *sandbox* directory for this ``Test``.  The resulting
        sandbox directory contains symlinks or copies of all the
        external/shared data dependencies of this ``Test``.

        See the :func:`.common.createSandbox` function for details on the
        arguments.

        :returns:         If this ``Test`` has no external data dependencies,
                          ``None`` is returned. Otherwise, the path to the
                          sandbox directory is returned.
        """

        return common.createSandbox(inputDir,
                                    self.__inputs,
                                    sandbox=sandbox,
                                    symlink=symlink)


    def __loadInputsFile(self):
        """Loads the all of the paths contained in the ``feedsInputs`` file,
        contained in this ``Test`` directory. Returns a list containing all
        of the paths. The returned list will be empty if this ``Test`` has no
        external data dependencies.
        """

        inputsFile = op.join(self.testDir, 'feedsInputs')

        if op.isfile(inputsFile):

            log.debug('Test {} - reading inputs from {}'.format(
                self.name, inputsFile))

            with open(inputsFile, 'rt') as f:

                # Make sure leading/trailing
                # whitespace and slashes, and
                # blank lines are removed
                inputs = list(f)
                inputs = [i.strip()       for i in inputs]
                inputs = [i.strip(op.sep) for i in inputs]
                inputs = [i               for i in inputs if i != '']
        else:
            inputs = []

        inputs = sorted(set(inputs))

        return inputs


def findTestDirs(path, depth=0):
    """Recursively finds all sub-directories in the given path which
    look like they contain a pyfeeds test.
    """

    path  = op.abspath(path)
    space = ' ' * depth

    log.debug('{}Searching for tests in {} ...'.format(space, path))

    testDirs = []

    # is this directory a test directory?
    if op.isfile(op.join(path, 'feedsRun')):
        log.debug('{}Found test directory: {}'.format(space, path))
        testDirs.append(path)

    # Gather a list of all sub-directories
    subDirs = [op.join(path, subDir) for subDir in os.listdir(path)]
    subDirs = [sd for sd in subDirs if op.isdir(sd)]

    # Recursively search for tests in the
    # sub-directories of this directory
    for sd in subDirs:
        testDirs.extend(findTestDirs(sd, depth + 1))

    return testDirs


def listTests(pyf):
    """Prints a list of all available tests.


    :arg pyf: A :class:`.Pyfeeds` instance
    """

    testNames = [t.name    for t in pyf.tests]
    testDirs  = [t.testDir for t in pyf.tests]
    titles    = ['Test name', 'Test directory']

    print('\nAvailable tests\n')
    common.printColumns(titles, [testNames, testDirs])


def bundleTests(pyf):
    """Creates a test *bundle* containing all of the given tests.

    :arg pyf: A :class:`.Pyfeeds` instance.
    """

    tests = pyf.tests

    bundleDir       = op.abspath(pyf.outputDir)
    inputDir        = op.abspath(pyf.inputDir)
    benchmarkDir    = op.abspath(pyf.benchmarkDir)
    bunTestDir      = op.join(bundleDir, 'tests')
    bunInputDir     = op.join(bundleDir, 'data')
    bunBenchmarkDir = op.join(bundleDir, 'benchmarks')

    if op.exists(bundleDir) and pyf.overwrite:
        shutil.rmtree(bundleDir)

    if op.exists(bundleDir):
        log.error('Bundle directory already exists ({})!'.format(bundleDir))
        sys.exit(1)

    os.makedirs(bunTestDir)

    if not pyf.skipInputDir:     os.makedirs(bunInputDir)
    if not pyf.skipBenchmarkDir: os.makedirs(bunBenchmarkDir)

    # We build a list of the inputs
    # for every test, and then pass
    # them to the common.createSandbox
    # function afterwards.
    inputs = []

    log.info('Copying tests to bundle ...')

    for i, test in enumerate(tests):

        log.debug('Copying test directory {} to bundle '
                  '(tests/{})'.format(test.testDir, test.name))

        shutil.copytree(test.testDir, op.join(bunTestDir, test.name))

        inputs.extend(test.getInputs())

    # Copy the test input data
    if not pyf.skipInputDir:
        log.info('Copying shared test data to bundle ...')
        common.createSandbox(inputDir,
                             inputs,
                             sandbox=bunInputDir,
                             symlink=False)

    # Copy the test benchmark data
    if not pyf.skipBenchmarkDir:
        log.info('Copying test benchmark data to bundle ...')

        for i, test in enumerate(tests):

            testBenchmarkDir = common.findPathIn(test.testDir, benchmarkDir)

            if testBenchmarkDir is None:
                log.debug('Could not find any benchmark '
                          'data for test {}'.format(test.name))
                continue

            destDir = op.relpath(testBenchmarkDir, benchmarkDir)

            log.debug('Copying test benchmark directory {} to bundle '
                      '(benchmarks/{})'.format(testBenchmarkDir, destDir))

            destDir   = op.join(bunBenchmarkDir, destDir)
            parentDir = op.split(destDir)[0]

            if not op.exists(parentDir):
                os.makedirs(parentDir)

            shutil.copytree(testBenchmarkDir, destDir)

    # Create a .feedsHashes
    # file if requested
    if not pyf.skipInputDir and pyf.genHashes:

        hashFile                = op.join(bunInputDir, '.feedsHashes')
        testHashes, inputHashes = hashing.calcHashes(tests, bunInputDir)

        hashes = {th : ih for th, ih in zip(testHashes, inputHashes)}

        hashing.saveHashes(hashFile, hashes)


def runTests(pyf):
    """Runs all of the given tests - see the :func:`runTest` function.

    :arg pyf: A :class:`.Pyfeeds` instance.
    """

    tests = pyf.tests

    inputDir     = op.abspath(pyf.inputDir)
    outputDir    = op.abspath(pyf.outputDir)
    benchmarkDir = op.abspath(pyf.benchmarkDir)
    hashFile     =            pyf.hashFile
    jobPool      = Pool(      pyf.jobs)
    startTime    = time.time()

    if op.exists(outputDir) and pyf.overwrite:
        shutil.rmtree(outputDir)

    if op.exists(outputDir):
        log.error('Output directory exists ({})!'.format(outputDir))
        sys.exit(1)

    if (pyf.sandboxDir is not None) and op.exists(pyf.sandboxDir):
        log.error('Sandbox directory exists ({})!'.format(outputDir))
        sys.exit(1)

    # Don't update hashes if
    # we're skipping hashes
    pyf.updateHashes &= (not pyf.skipHashes)

    if hashFile is None:
        hashFile = op.join(inputDir, '.feedsHashes')

    hashFile = op.abspath(hashFile)

    if not pyf.skipHashes:
        testHashes = hashing.loadHashes(hashFile)

    log.info('{} tests to run'.format(len(tests)))

    # Make sure that the pyfeeds directory
    # is on the python path, so that individual
    # tests have access to the pyfeeds package
    # namespace if they wish
    thisDir           = op.join(op.dirname(op.realpath(__file__)), '..')
    env               = os.environ.copy()
    env['PYTHONPATH'] = op.pathsep.join([thisDir, env.get('PYTHONPATH', '')])

    # For each test we store a dictionary containing
    # the results of running the test. Each result
    # dict contains:
    #
    #   - 'test'      - The Test object
    #   - 'hash_code' - Test hash code (see hashing.checkTestHash)
    #   - 'exit_code' - Test process exit code
    #   - 'time'      - Number of seconds taken to run the test
    #
    # These are then passed through to the
    # evaluate.evaluateTest function, to
    # evaluate the test.
    testResults = [{} for t in tests]
    for i, test in enumerate(tests):
        testResults[i]['test']      = test
        testResults[i]['hash_code'] = hashing.TEST_HASH_NOT_CHECKED

    # Verify the input data
    # hash for every test
    if not pyf.skipHashes:

        # Do it in parallel using the job pool.
        jobArgs = [(pyf, t, inputDir, testHashes, pyf.updateHashes)
                   for t in tests]
        results = jobPool.map(common.starmap(hashing.checkTestHash), jobArgs)

        # Update the test result dicts
        for i, (test, result) in enumerate(zip(tests, results)):
            testResults[i]['hash_code'] = result

    # Run each test. Build a list of
    # arguments to pass to the runTest
    # function for every test.
    jobArgs = []
    for test in tests:

        if pyf.sandboxDir is None:
            sandbox = None
        else:

            sandbox = op.abspath(op.join(pyf.sandboxDir, test.name))

            if op.exists(sandbox):
                log.debug('Removing old sandbox '
                          'directory {}'.format(sandbox))
                shutil.rmtree(sandbox)

        jobArgs.append((
            pyf,
            test,
            outputDir,
            inputDir,
            benchmarkDir,
            env,
            pyf.leaveSandboxes,
            sandbox))

    # Then run the tests
    # using the job pool.
    results = jobPool.map(common.starmap(runTest), jobArgs)
    endTime = time.time()
    minutes = (endTime - startTime) / 60.0

    # Copy the test results and runtimes
    # to the TestResult objects
    for i, (test, (result, runtime)) in enumerate(zip(tests, results)):

        testResults[i]['result'] = result
        testResults[i]['time']   = runtime

    # Then arrange the test result
    # info into separate columns
    titles  = ['Test', 'Time (seconds)', 'Result', 'Data status']
    columns = [
        [r['test'].name                                  for r in testResults],
        [r['time']                                       for r in testResults],
        ['Passed' if r['result'] else 'Failed'           for r in testResults],
        [hashing.TEST_HASH_SHORT_STRINGS[r['hash_code']] for r in testResults]]

    # And print them all out nicely
    common.printColumns(titles, columns)

    passed = sum([r['result'] for r in testResults])
    log.info('{} / {} tests passed in {:0.2f} minutes'.format(
        passed, len(testResults), minutes))

    if pyf.updateHashes:
        hashing.saveHashes(hashFile, testHashes)


def runTest(pyf,
            test,
            outputDir,
            inputDir,
            benchmarkDir,
            env,
            leaveSandbox,
            sandboxDir=None):
    """Runs the given :class:`Test`. The test is executed, and then passed to
    the :func:`.evaluateTest` function to determine whether it passed or
    failed.

    :returns: A tuple containing:

                - ``True`` if the test passed, ``False`` otherwise.
                - Number of seconds taken to run the test

    :arg pyf:          The :class:`.Pyfeeds` instance.

    :arg test:         The test.

    :arg outputDir:    Output directory.

    :arg inputDir:     Directory containing test input data.

    :arg benchmarkDir: Directory containing test benchmark data.

    :arg env:          Dictionary containing the environment variables to be
                       passed to the test process.

    :arg leaveSandbox: If ``True``, the sandbox directory created for the test
                       (if any) is not deleted.

    :arg sandboxDir:   Directory to be used as the test sandbox. See the
                       ``sandbox`` parameter to :meth:`Test.createSandbox`.
    """

    runTime = 0

    try:

        sandboxDir   = test.createSandbox(inputDir, sandbox=sandboxDir)
        outputDir    = op.realpath(op.join(outputDir, test.name))
        benchmarkDir = common.findPathIn(test.testDir, benchmarkDir)

        log.info( 'Running test {} ...'.format(test.name))
        log.debug('   input directory:     {}'.format(sandboxDir))
        log.debug('   output directory:    {}'.format(outputDir))
        log.debug('   benchmark directory: {}'.format(benchmarkDir))

        if op.isdir(outputDir):

            log.debug('Deleting old test output directory: {}'.format(
                outputDir))
            shutil.rmtree(outputDir)

        log.debug('(Re-)Creating test output directory: {}'.format(outputDir))
        os.makedirs(outputDir)

        cmd = [test.testScript, outputDir, sandboxDir, benchmarkDir]
        cmd = [str(c) for c in cmd]

        start = time.time()

        with open(op.join(outputDir, 'feedsRun.log'), 'wt') as logFile:

            log.debug('Calling process "{}"'.format(' '.join(cmd)))

            retcode = subprocess.call(cmd,
                                      env=env,
                                      cwd=test.testDir,
                                      stdout=logFile,
                                      stderr=logFile)

        runTime = int(time.time() - start)
        result  = evaluate.evaluateTest(pyf,
                                        test,
                                        retcode,
                                        outputDir,
                                        benchmarkDir)

        if result: status = 'passed'
        else:      status = 'failed'

        log.info('Test {} {} in {} seconds'.format(test, status, str(runTime)))

        if (sandboxDir is not None) and (not leaveSandbox):
            log.debug('Deleting sandbox for test {}: {}'.format(
                test, sandboxDir))
            shutil.rmtree(sandboxDir)

        return result, runTime

    except Exception as e:

        log.warning('Test {} crashed: {}'.format(test.name, str(e)),
                    exc_info=True)

        return False, runTime
