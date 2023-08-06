import cloudpickle as cp
import sys
from py4j.java_gateway import JavaGateway, GatewayParameters

from twister2.tset.TSet import TSet
from twister2.tset.fn.SourceFunc import SourceFunc
from twister2.tset.fn.factory.TSetFunctions import TSetFunctions
from twister2.utils import SourceWrapper


class Twister2Environment:

    def __init__(self):
        print("Connecting to java port %s" % sys.argv[1])
        gateway = JavaGateway(gateway_parameters=GatewayParameters(port=int(sys.argv[1])))
        self.__entrypoint = gateway.entry_point
        self.__predef_functions = TSetFunctions(self.__entrypoint.functions(), self)

    @property
    def config(self):
        return self.__entrypoint.getConfig()

    @property
    def worker_id(self):
        return self.__entrypoint.getWorkerId()

    @property
    def functions(self) -> TSetFunctions:
        return self.__predef_functions

    def create_source(self, source_function: SourceFunc, parallelism=0) -> TSet:
        if not isinstance(source_function, SourceFunc):
            raise Exception('source_function should be an instance of {}'.format(SourceFunc))

        source_function_wrapper = SourceWrapper(source_function)

        java_src_ref = self.__entrypoint.createSource(cp.dumps(source_function_wrapper), parallelism)
        src_tset = TSet(java_src_ref, self)
        return src_tset
