from docutils import nodes
from docutils.parsers.rst import Directive
from runcible.core.plugin_registry import PluginRegistry
from sphinx import directives


class RuncibleDriverDocs(Directive):
    has_content = True
    required_arguments = 1

    def run(self):
        PluginRegistry.load_drivers()
        driver_class = PluginRegistry.get_driver(self.arguments[0])
        title_node = directives.nodes.title(text="Modules")
        module_nodes = self.gen_driver_nodes(driver_class)
        # module_nodes = []
        # for provider_name, options in driver_class.module_provider_map.items():
        #     module_nodes.append(directives.nodes.subtitle(text=provider_name + ':'))
        #     module_nodes.append(directives.nodes.paragraph(text="Supported Attributes:"))
        #     table = directives.nodes.table()
        #     module_nodes.append(table)
        #     module_nodes.append(self.create_table(header=('Attribute',
        #                                                   'Type',
        #                                                   'Allowed Operations')))

        return [title_node] + module_nodes

    def gen_driver_nodes(self, driver_class):
        header = ("Attribute", "Type", "Allowed Operations", "Description", "Examples")
        colspec = (1, 1, 2, 2, 3)
        # table = self.create_table()
        # data = []
        nodes = []
        for provider_name, provider in driver_class.module_provider_map.items():
            nodes.append(directives.nodes.subtitle(text=provider_name + ':'))
            nodes.append(directives.nodes.paragraph(text="Supported Attributes:"))

            # Get data to build tables
            data = []
            for attribute in provider.supported_attributes:
                module = provider.provides_for
                attribute_name = attribute
                attribute_type = self.get_type_string(module.configuration_attributes[attribute]['type'])
                attribute_allowed_ops_list = self.get_formatted_oplist(module.configuration_attributes[attribute]['allowed_operations'])
                if module.configuration_attributes[attribute].get('examples', None) is not None:
                    attribute_examples = self.format_examples(module.configuration_attributes[attribute].get('examples', None))
                else:
                    attribute_examples = None
                attribute_description = module.configuration_attributes[attribute].get('description', None)
                data.append((attribute_name, attribute_type, attribute_allowed_ops_list, attribute_description, attribute_examples))
            nodes.append(self.create_table(header=header, data=data, colspec=colspec))
        return nodes

    def format_examples(self, example_list):
        join_list = []
        for item in example_list:
            if type(item) is not str:
                join_list.append(str(item))
            else:
                join_list.append(item)
        return ', '.join(join_list)

    def get_type_string(self, type):
        if type is str:
            return "string"
        elif type is int:
            return "integer"
        elif type is list:
            return "list"
        elif type is bool:
            return "boolean"
        elif type is dict:
            return "dict"

    def get_formatted_oplist(self, oplist: list):
        op_list = []
        for operation in oplist:
            op_list.append(operation.name)
        return ', '.join(op_list)

    def create_table(self, header: tuple, data: list, colspec: tuple):
        # header = ("Attribute", "Default")
        colwidths = colspec
        # data = [
        #     ("attr1", "True"),
        #     ("attr2", "False")
        # ]
        table = directives.nodes.table()
        tgroup = nodes.tgroup(cols=len(header))
        table += tgroup
        for colwidth in colwidths:
            tgroup += nodes.colspec(colwidth=colwidth)

        thead = nodes.thead()
        tgroup += thead
        thead += self.create_table_row(header)
        tbody = directives.nodes.tbody()
        tgroup += tbody
        for data_row in data:
            tbody += self.create_table_row(data_row)
        return table

    def create_table_row(self, row_cells):
        row = directives.nodes.row()
        for cell in row_cells:
            entry = directives.nodes.entry()
            row += entry
            entry += nodes.paragraph(text=cell)
        return row

def setup(app):
    app.add_directive("runcible_driver", RuncibleDriverDocs)

    return {
        'version': '0.2',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }