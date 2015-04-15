#!/bin/bash

# Run the samples in $1/doc/code_sample.
# This works by adding, temporarily, test file referencing them, testing, and
# deleting it.
# If the test fails, then the test file lingers, which might make debugging
# easier.

# $1/doc/code_sample must contain a file "test-preamble.cpp" that contains all
# the includes, and a "BOOST_AUTO_TEST_SUITE" header.

set -o nounset
set -o errexit

Project=$1

SourcePath=${Project}/doc/code_sample
TestPath=${Project}/test/${Project}
TestCodeSamples=test-code_samples
TestFile=${TestPath}/${TestCodeSamples}.cpp

cat ${SourcePath}/test-preamble.cpp > ${TestFile}

for Sample in `find ${SourcePath} -name '*.ipp'`
do
    TestNames=`basename ${Sample} .ipp`
    echo 'BOOST_AUTO_TEST_CASE (' ${TestNames} ') {' >> ${TestFile}
    echo '#   include "'../../../${Sample}'"' >> ${TestFile}
    echo '}' >> ${TestFile}
    echo '' >> ${TestFile}
done

echo 'BOOST_AUTO_TEST_SUITE_END()' >> ${TestFile}

cd $TestPath
bjam ${TestCodeSamples}
rm ${TestCodeSamples}.cpp
