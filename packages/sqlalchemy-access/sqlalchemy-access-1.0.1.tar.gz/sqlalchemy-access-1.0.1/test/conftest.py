from sqlalchemy.dialects import registry

registry.register("access.pyodbc", "sqlalchemy_access.pyodbc", "AccessDialect_pyodbc")


from sqlalchemy.testing.plugin.pytestplugin import *
