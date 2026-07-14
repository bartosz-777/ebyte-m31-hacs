"""Test runner for Ebyte M31 hub using mocked dependencies."""
import asyncio
import sys
import types

# Create fake homeassistant.const module
homeassistant = types.ModuleType("homeassistant")
homeassistant.const = types.SimpleNamespace(CONF_HOST="host", CONF_PORT="port")
sys.modules["homeassistant"] = homeassistant
sys.modules["homeassistant.const"] = homeassistant.const

# Create fake pymodbus package
pymodbus = types.ModuleType("pymodbus")
# exceptions submodule
exceptions = types.SimpleNamespace(ModbusException=Exception)
# client submodule with ModbusTcpClient
class FakeResult:
    def __init__(self, bits):
        self.bits = bits
    def isError(self):
        return False

class FakeClient:
    def __init__(self, host=None, port=None, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout

    def connect(self):
        return True

    def read_discrete_inputs(self, address=0, count=8, slave=1):
        # return an object with .bits and .isError()
        return FakeResult([1 if i % 2 == 0 else 0 for i in range(count)])

    def close(self):
        pass

pymodbus.client = types.SimpleNamespace(ModbusTcpClient=FakeClient)
sys.modules["pymodbus"] = pymodbus
sys.modules["pymodbus.client"] = pymodbus.client
sys.modules["pymodbus.exceptions"] = exceptions

# Ensure package path
import importlib
import importlib.util
import os
pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def import_module_from_path(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


async def main():
    # Prepare a fake package context and preload const module so relative imports work
    package_dir = os.path.join(pkg_root, "custom_components", "ebyte_m31")
    # create package modules
    pkg_name = "custom_components"
    subpkg_name = "custom_components.ebyte_m31"
    import types as _types
    if pkg_name not in sys.modules:
        sys.modules[pkg_name] = _types.ModuleType(pkg_name)
    if subpkg_name not in sys.modules:
        mod = _types.ModuleType(subpkg_name)
        mod.__path__ = [package_dir]
        sys.modules[subpkg_name] = mod

    # preload const module
    const_path = os.path.join(package_dir, "const.py")
    import_module_from_path(subpkg_name + ".const", const_path)

    # Import the hub module within the package context
    hub_path = os.path.join(package_dir, "hub.py")
    hub_mod = import_module_from_path(subpkg_name + ".hub", hub_path)
    # instantiate hub
    hub = hub_mod.EbyteM31Hub("127.0.0.1", 502)
    # call async_read_discrete_inputs
    vals = await hub.async_read_discrete_inputs()
    print("Read discrete inputs:", vals)
    # validate protocol
    try:
        await hub.async_validate_modbus_protocol()
        print("async_validate_modbus_protocol: OK")
    except Exception as e:
        print("async_validate_modbus_protocol: ERROR", e)

if __name__ == "__main__":
    asyncio.run(main())
