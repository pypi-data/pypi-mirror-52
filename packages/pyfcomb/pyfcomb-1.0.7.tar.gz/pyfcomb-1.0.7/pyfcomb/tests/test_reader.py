import pytest
from pyfcomb import _solution_strings

@pytest.mark.parametrize('value',[
    ('f17=1f2+2f1',['f17=2f1+1f2'],('f17 =   f2 + 2*f1', None)),
    ('f35=1f13-1f1',[],('f35 =   f13 - f1', None)),
])
def testSolutionStrings(value):
    assert _solution_strings(value[0],value[1]) == value[2]

