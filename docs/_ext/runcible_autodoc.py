from docutils import nodes
from docutils.parsers.rst import Directive
from runcible.core.plugin_registry import PluginRegistry
from runcible.providers.provider_array import ProviderArrayBase
from runcible.providers.provider import ProviderBase
from sphinx import directives
import yaml

dump_noalias = yaml.dumper.SafeDumper
dump_noalias.ignore_aliases = lambda self, data: True


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
        # table = self.create_table()
        # data = []
        nodes = []
        for provider_name, provider in driver_class.module_provider_map.items():
            nodes.append(directives.nodes.subtitle(text=provider_name + ':'))
            if issubclass(provider, ProviderBase) and not issubclass(provider, ProviderArrayBase):
                nodes.append(directives.nodes.paragraph(text='Type: Module'))
                nodes.append(directives.nodes.paragraph(text="Supported Attributes:"))
                nodes.append(self.populate_column(provider))
                example_yaml = self.get_module_example(provider)
                nodes.append(directives.nodes.literal_block(example_yaml, example_yaml))
            if issubclass(provider, ProviderArrayBase):
                nodes.append(directives.nodes.paragraph(text='Type: Module Array'))
                nodes.append(directives.nodes.paragraph(text="Supported Attributes:"))
                nodes.append(self.populate_column(provider.sub_module_provider))
                example_yaml = self.get_module_array_example(provider)
                nodes.append(directives.nodes.literal_block(example_yaml, example_yaml))

        return nodes

    def populate_column(self, provider):
        header = ("Attribute", "Type", "Allowed Operations", "Description", "Examples")
        colspec = (1, 1, 2, 2, 3)
        data = []
        for attribute in provider.supported_attributes:
            module = provider.provides_for
            attribute_name = attribute
            attribute_type = self.get_type_string(module.configuration_attributes[attribute]['type'])
            attribute_allowed_ops_list = self.get_formatted_oplist(
                module.configuration_attributes[attribute]['allowed_operations'])
            if module.configuration_attributes[attribute].get('examples', None) is not None:
                attribute_examples = module.configuration_attributes[attribute].get('examples', None)
            else:
                attribute_examples = None
            attribute_description = module.configuration_attributes[attribute].get('description', None)
            data.append(
                (attribute_name, attribute_type, attribute_allowed_ops_list, attribute_description, attribute_examples))
        return self.create_table(header=header, data=data, colspec=colspec)

    def get_module_array_example(self, provider):
        module = provider.provides_for
        example_dict = {module.module_name: []}
        example_item = {}
        for attribute in provider.sub_module_provider.supported_attributes:
            if module.sub_module.configuration_attributes[attribute].get('examples', None) is not None:
                example_item.update({attribute: module.sub_module.configuration_attributes[attribute]['examples'][0]})
        example_dict[module.module_name].append(example_item)
        yaml_string = yaml.dump(example_dict, default_flow_style=False, Dumper=dump_noalias)
        output = f"# Example Runcible {module.module_name} module array\n---\n" + yaml_string
        return output

    def get_module_example(self, provider):
        module = provider.provides_for
        example_dict = {module.module_name: {}}
        for attribute in provider.supported_attributes:
            if module.configuration_attributes[attribute].get('examples', None) is not None:
                example_dict[module.module_name].update({attribute: module.configuration_attributes[attribute]['examples'][0]})
        yaml_string = yaml.dump(example_dict, default_flow_style=False, Dumper=dump_noalias)
        output = f"# Example Runcible {module.module_name} module\n---\n" + yaml_string
        return output

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
        return op_list

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
            if type(cell) is list:
                bulletlist = directives.nodes.bullet_list()
                for item in cell:
                    i_bullet = directives.nodes.list_item()
                    i_bullet += directives.nodes.paragraph(text=item)
                    bulletlist += i_bullet
                entry = directives.nodes.entry()
                row += entry
                entry += bulletlist
            else:
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