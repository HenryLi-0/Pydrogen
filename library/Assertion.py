from library.FaultLogger import FaultLogger
from library.FaultLogger import FaultType

'''
ref: https://github.com/SciBorgs/Hydrogen/blob/main/src/main/java/org/sciborgs1155/lib/Assertion.java
'''

class Assertion:
    @staticmethod
    def reportTrue(condition:bool, faultName:str, desc:str) -> None:
        '''
        Asserts that a condition is true and reports to FaultLogger.
         - `condition`
         - `faultName`
         - `description`
        '''
        FaultLogger.reportFaultData(
            faultName,
            ("success!" if condition else "") + desc,
            FaultType.INFO if condition else FaultType.WARNING
        )

    @staticmethod
    def reportEquals(faultName:str, expected:float, actual:float, delta:float) -> None:
        '''
        Asserts that two values are equal (with some tolerance) and reports to FaultLogger.
        - `faultName`
        - `expected`
        - `actual`
        - `delta tolerance`
        '''
        Assertion.reportTrue(
            abs(expected - actual) <= delta,
            faultName,
            "expected: " + str(expected) + "; actual: " + str(actual)
        )
    
    # TODO truthassertion and equalityassertion not implemented yet, not sure if its necessary?