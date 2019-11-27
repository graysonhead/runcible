from runcible.modules.module_array import ModuleArray
from runcible.modules.static_v4_route import StaticV4Route, StaticV4RouteResources


class StaticV4Routes(ModuleArray):
    module_name = 'static_v4_routes'
    sort_key = StaticV4RouteResources.PREFIX
    sub_module = StaticV4Route