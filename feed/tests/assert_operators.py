"""
Look away! this just turns the operators in the operator modules into
functions of the same name that assert their own truth. Codegen FTW.
This uses the exec function, which is insane and ugly. but types.FunctionTpe/types.CodeType is insane, ugly, AND very tedious
"""
import operator
from string import Template

INTERESTING_OPS = [
'and_',
'contains',
'eq',
'ge',
'gt',
'isCallable',
'isMappingType',
'isNumberType',
'isSequenceType',
'is_',
'is_not',
'le',
'lt',
'ne',
'not_',
'or_',
'repeat',
'sequenceIncludes',
'truth']

FUNCTION_TEMPLATE = Template("""
def $op_name(*args, **kwargs):
    assert operator.$op_name(*args, **kwargs)
""")

for op_name in INTERESTING_OPS:
    exec(FUNCTION_TEMPLATE.substitute(op_name=op_name))
 