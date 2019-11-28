from runcible.modules.module_array import ModuleArray
from runcible.modules.static_v4_interface_route import StaticV4InterfaceRoute, StaticV4RouteInterfaceResources


class StaticV4InterfaceRoutes(ModuleArray):
    module_name = 'static_v4_routes'
    sort_key = StaticV4RouteInterfaceResources.PREFIX
    sub_module = StaticV4InterfaceRoute
