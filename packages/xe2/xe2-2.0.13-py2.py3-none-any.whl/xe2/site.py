#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# @copyright Copyright (C) Guichet Entreprises - All Rights Reserved
# 	All Rights Reserved.
# 	Unauthorized copying of this file, via any medium is strictly prohibited
# 	Dissemination of this information or reproduction of this material
# 	is strictly forbidden unless prior written permission is obtained
# 	from Guichet Entreprises.
###############################################################################

###############################################################################
# standard object to wrap file and access easily to the filename
#
###############################################################################

import logging
import sys
import os
import os.path
import shutil
import copy
import networkx as nx

import mdtools.common as common
import mdtools.mdcommon as mdcommon
from mdtools.mdfile import MarkdownContent


if (__package__ in [None, '']) and ('.' not in __name__):
    import page
    import resource
    import menu
else:
    from . import page
    from . import resource
    from . import menu

###########################################################################
# Test a node data
#
# @param graph the graph
# @param key the node key
# @param value the node data to test
# @return the test
###########################################################################
def test_node(graph, key, value):
    if key not in graph.nodes:
        return False
    return value in graph.nodes[key] and graph.nodes[key][value]


###########################################################################
# compute the url link between two file
#
# @param source the source file or folder
# @param dest the destination file
# @return the url relative
###########################################################################
def compute_url(source, dest, source_is_file=None):
    source_folder = source

    # suppose to be testable
    if (source_is_file is not None and source_is_file) or \
            os.path.isfile(source_folder):
        (source_folder, _unused) = os.path.split(source_folder)

    result = os.path.relpath(dest, source_folder)
    result = result.replace("\\", "/")

    # print("source=%s" % source)
    # print("dest  =%s" % dest)
    # print("url   =%s" % result)

    return result


def test_compute_url():
    source = "/a/b/c/"
    destin = "/a/b/c/d/e/f.md"
    # print(compute_url(source, destin))
    assert compute_url(source, destin) == "d/e/f.md"

    source = r"c:\dev\projet-ge.fr\win-tools\xenon2\examples" \
        r"\example05\input-md"
    destin = r"c:\dev\projet-ge.fr\win-tools\xenon2\examples" \
        r"\example05\input-md\footer\./xx/page.md"
    # print(compute_url(source, destin))
    assert compute_url(source, destin) == "footer/xx/page.md"

    source = r"c:\dev\projet-ge.fr\win-tools\xenon2\examples" \
        r"\example05\output\index.html"
    destin = r"c:\dev\projet-ge.fr\win-tools\xenon2\examples" \
        r"\example05\output"
    print(compute_url(source, destin))
    # # assert compute_url(source, destin) == "footer/xx/page.md"

###########################################################################
# adjust links between two file inside the site
#
# @param resources the graph resources
###########################################################################
def adjust_link_url(resources):
    for (src, dest) in resources.edges:
        if test_node(resources, src, 'is_on_filesystem') and \
                test_node(resources, dest, 'is_on_filesystem'):
            link = resources.edges[src, dest]['link']
            file_src = resources.nodes[src]['target_resource'].full_filename
            file_dest = resources.nodes[dest]['target_resource'].full_filename
            link.url = compute_url(file_src, file_dest,
                                   source_is_file=True)

###########################################################################
# copy all resources to the target and change links
#
# @param resources the graph resources
# @param key the node key
# @param target_folder the folder to copy the resources
# @return the filename of the target
###########################################################################
def copy_node_resource_to_target(resources, key, target_folder):
    target_folder = common.check_create_folder(target_folder)

    if not test_node(resources, key, 'is_on_filesystem'):
        return None

    source = resources.nodes[key]['resource']
    dest = resource.Resource(os.path.join(target_folder,
                                          source.relative_filename),
                             target_folder)

    # change of the target
    if dest.filename_ext == ".md":
        dest.filename_ext = ".html"

    resources.nodes[key]['target_resource'] = dest
    return dest.full_filename

###########################################################################
# copy all resources to the target and change links
#
# @param resources the graph resources
# @param target_folder the folder to copy the resources
# @return empty
###########################################################################
def copy_resources_to_target(resources, target_folder):
    target_folder = common.check_create_folder(target_folder)
    for key in resources:
        if test_node(resources, key, 'is_on_filesystem'):
            copy_node_resource_to_target(resources, key, target_folder)

###########################################################################
# Add a page node
#
# @param filename the filename of the md file to start
# @param parent_filename the filename of the md file parent
###########################################################################
def add_external_link(resources, target_url,
                      node_id_source=None, initial_link=None):
    is_web_link = False

    if mdcommon.is_external_link(target_url):
        is_web_link = True
        target_url = mdcommon.get_domain_name(target_url)
    else:
        logging.info('Unidentify resource %s from %s',
                     target_url, repr(node_id_source))
        source_start_path = resources.graph['source_root_path']
        if node_id_source is not None:
            source_start_path = \
                resources.nodes[node_id_source]['resource'].filename_path
        target_file = os.path.join(source_start_path, target_url)
        target_url = common.set_correct_path(target_file)
        logging.info('Trying to add %s', target_url)

    if target_url not in resources:
        resources.add_node(target_url, is_link=is_web_link)

    if node_id_source is not None:
        resources.add_edge(node_id_source,
                           target_url, link=initial_link)

    return target_url


###############################################################################
# Process instruction footer
###############################################################################
def instruction_home(key, value, site, md_file):
    if key != "home":
        return

    if 'home_key' in site.resources.graph:
        logging.warning("home declared for the second time in %s",
                        md_file.relative_filename)

    logging.info("find the home in %s", md_file.full_filename)
    site.resources.graph['home_key'] = md_file.relative_filename
    site.resources.nodes[md_file.relative_filename]['breadcrumb'] = value


###############################################################################
# Process instruction footer
###############################################################################
def instruction_menu(key, value, site, md_file):
    if key != "menu":
        return
    if 'menu' in site.resources.graph:
        logging.warning("menu declared for the second time in %s",
                        md_file.relative_filename)

    general_menu = menu.read_menu(
        md_filename=os.path.join(md_file.filename_path, value),
        base_path=md_file.base_path)
    print("-------------------")
    print(general_menu)
    print("-------------------")
    site.resources.graph['menu'] = general_menu

    # add page
    def add_page(link):
        if ('url' in link) and (link['url'] not in site.resources):
            site.add_page_node(link['url'])

    general_menu.apply(add_page)

###############################################################################
# Process instruction footer
###############################################################################
def prepare_breadcrumb_links(page_key, resources):
    logging.info("prepare the breadcrumb links for %s", page_key)
    steps = []
    if 'home_key' not in resources.graph:
        return {'steps': steps}

    start_key = resources.graph['home_key']
    page_node_fs = resources.nodes[page_key]['target_resource'].full_filename

    try:
        sh_path = nx.shortest_path(resources, start_key, page_key)
    except nx.NetworkXNoPath:
        sh_path = [start_key, page_key]

    for key in sh_path:
        current_node = resources.nodes[key]
        current_fs = current_node['target_resource'].full_filename
        url = compute_url(page_node_fs, current_fs, source_is_file=True)
        name = current_node['title']
        if 'breadcrumb' in current_node:
            name = current_node['breadcrumb']
        steps.append({"name": name, "url": url})

    steps[-1]['active'] = ""

    return {'steps': steps}

###############################################################################
# Process instruction footer
###############################################################################
def prepare_menu_links(page_key, resources):
    logging.info("prepare the menu links for %s", page_key)
    if 'menu' not in resources.graph:
        return []

    start_menu = copy.deepcopy(resources.graph['menu'])
    page_node_fs = resources.nodes[page_key]['target_resource'].full_filename

    def change_link(link):
        if link.url is None or mdcommon.is_external_link(link.url):
            return
        if link.url not in resources:
            logging.warning("In the general menu, "
                            "the link [%s](%s) leads to nowhere",
                            link.label, link.url)
            return
        link_node = resources.nodes[link.url]
        link_fs = link_node['target_resource'].full_filename
        link.url = compute_url(page_node_fs, link_fs, source_is_file=True)

    start_menu.apply(change_link)

    return start_menu

###############################################################################
# Process instruction footer
###############################################################################
def instruction_footer(key, value, site, md_file):
    if key != "footer":
        return

    logging.info("find the footer in %s", md_file.full_filename)
    footer_file = os.path.join(md_file.filename_path, value)
    footer_file = common.check_is_file_and_correct_path(footer_file)
    logging.info("footer declared is %s", footer_file)

    if 'footer_links_node' in site.resources.graph:
        logging.warning("footer declared for the second time in %s",
                        footer_file)

    footer_content = common.get_file_content(footer_file)
    footer_content = menu.preprocess_menu_add_label(
        footer_content, os.path.split(footer_file)[0])
    links = mdcommon.search_link_in_md_text(footer_content)

    # process link
    for link in links:
        dest_file = os.path.join(os.path.split(footer_file)[0], link['url'])
        target_url = compute_url(site.source_root_path, dest_file,
                                 source_is_file=False)
        logging.info("Add (for the footer links) the file %s", target_url)
        result_integration = site.add_page_node(target_url)
        logging.info("     Integration result is %s", result_integration)
        if 'footer_links_node' not in site.resources.graph:
            site.resources.graph['footer_links_node'] = []

        site.resources.graph['footer_links_node'].append(
            {'key': result_integration, 'link': link})

###############################################################################
# Process instruction footer
###############################################################################
def prepare_footer_links(page_location, resources):
    logging.info("prepare the footer links for %s", page_location)
    result = []
    if 'footer_links_node' not in resources.graph:
        return result
    footer_links_node = resources.graph['footer_links_node']

    for flink in footer_links_node:
        final_link = flink['link']
        # change the url in case of a real file
        if test_node(resources, flink['key'], 'is_on_filesystem'):
            dest_filename = resources.nodes[flink['key']]['target_resource']
            final_link['url'] = compute_url(page_location,
                                            dest_filename.full_filename,
                                            source_is_file=True)

        result.append(final_link)

    return result

###############################################################################
# Process instruction for saving the data
###############################################################################
def instruction_save_value(key, value, site, _unused_md_file):
    site.context[key] = value


###############################################################################
# get the instruction from name
###############################################################################
@common.static(__inst__=None)
def site_instruction(name):
    if site_instruction.__inst__ is None:
        site_instruction.__inst__ = {}
        site_instruction.__inst__['footer'] = instruction_footer
        site_instruction.__inst__['home'] = instruction_home
        site_instruction.__inst__['menu'] = instruction_menu

    if name not in site_instruction.__inst__:
        return instruction_save_value

    return site_instruction.__inst__[name]


###############################################################################
# An object to rule the web site
###############################################################################
class WebSite:

    ###########################################################################
    # Initialize the object from a content a filename or other
    #
    # @param start_point the filename of the md file to start
    ###########################################################################
    def __init__(self, start_point, jinja_env=None, context=None,
                 internal_dep=None):
        source_root_path = start_point
        if not os.path.isdir(source_root_path):
            source_root_path = os.path.split(source_root_path)[0]

        self.__context = context
        self.__env = jinja_env
        self.__resources = nx.DiGraph(source_root_path=source_root_path)
        self.__internal_dep = internal_dep

        # set default value
        if self.__env is None:
            self.__env = page.get_default_jinja_env()
        if self.__internal_dep is None:
            self.__internal_dep = page.get_default_resources()
        if self.__context is None:
            self.__context = {}

        logging.info("create awebsite with start folder = %s",
                     source_root_path)

        if os.path.isfile(start_point):
            self.add_page_node(start_point)

    ###########################################################################
    # Add a page node
    #
    # @param filename the filename of the md file to start
    # @param parent_filename the filename of the md file parent
    ###########################################################################
    def process_md_intergation(self, md_resource):
        if md_resource.filename_ext != ".md":
            return

        the_md = MarkdownContent(md_resource.full_filename)
        data = self.resources.nodes[md_resource.relative_filename]

        data['title'] = the_md.title

        for key in the_md:
            key_split = key.split(":")
            main_key = key_split[0].lower()
            inst_name = key_split[1].lower() if len(key_split) > 1 else None
            if main_key == "site" and inst_name is not None:
                site_instruction(inst_name)(inst_name, the_md[key],
                                            self, md_resource)
            if main_key == "page" and inst_name is not None:
                data[inst_name] = the_md[key]

        links = mdcommon.search_link_in_md_file(md_resource.full_filename)
        # process link
        for link in links:
            self.add_page_node(link['url'],
                               node_id_source=md_resource.relative_filename,
                               initial_link=mdcommon.Link(**link))

    ###########################################################################
    # Add a page node
    #
    # @param filename the filename of the md file to start
    # @param parent_filename the filename of the md file parent
    ###########################################################################
    def add_page_node(self, target_url,
                      node_id_source=None, initial_link=None):
        logging.info("Add the resource %s", target_url)
        source_start_path = self.source_root_path

        if node_id_source is not None:
            source_start_path = \
                self.resources.nodes[node_id_source]['resource'].filename_path

        target_file = os.path.join(source_start_path, target_url)
        target_file = common.set_correct_path(target_file)

        # case if the target is not on the filesystem
        if not os.path.isfile(target_file):
            logging.info(
                "    the resource %s is not a file (external link)", target_url)
            return add_external_link(self.resources, target_url,
                                     node_id_source=node_id_source,
                                     initial_link=initial_link)

        # case if the target IS ON the filesystem
        the_file = resource.Resource(target_file,
                                     base_path=self.source_root_path)

        if the_file.relative_filename not in self.resources:
            test_md = the_file.filename_ext == ".md"
            self.resources.add_node(the_file.relative_filename,
                                    resource=the_file,
                                    is_on_filesystem=True,
                                    is_md=test_md)
            if test_md:
                self.process_md_intergation(the_file)

        if node_id_source is not None:
            self.resources.add_edge(node_id_source,
                                    the_file.relative_filename,
                                    link=initial_link)

        return the_file.relative_filename

    ###########################################################################
    # Add a page node
    #
    # @param filename the filename of the md file to start
    # @param parent_filename the filename of the md file parent
    ###########################################################################
    def create_internal_dep(self, target_folder):
        self.context['lib_image'] = {}
        for res_group in self.internal_dep:
            res_group.copy(target_folder)
            images = res_group.build_lib([".png", '.jpg'])
            for key in images:
                self.context['lib_image'][key] = images[key]

    ###########################################################################
    # Add a page node
    #
    # @param filename the filename of the md file to start
    # @param parent_filename the filename of the md file parent
    ###########################################################################
    def create_site(self, target_folder):
        target_folder = common.check_create_folder(target_folder)
        copy_resources_to_target(self.resources, target_folder)
        self.create_internal_dep(target_folder)
        adjust_link_url(self.resources)
        self.context['root_web_site'] = target_folder
        for key in self.resources:
            self.create_page(key, target_folder)

    ###########################################################################
    # Add a page node
    #
    # @param filename the filename of the md file to start
    # @param parent_filename the filename of the md file parent
    ###########################################################################
    def get_context_for_page(self, key, target_folder):
        result = copy.deepcopy(self.__context)
        dest = self.resources.nodes[key]['target_resource']

        if 'home_key' in self.resources.graph:
            home_key = self.resources.graph['home_key']
            if home_key in self.resources.nodes:
                home_node = self.resources.nodes[home_key]
                if 'title' in home_node:
                    result['home_page_title'] = home_node['title']

        result['root_path'] = compute_url(dest.full_filename,
                                          target_folder, source_is_file=True)
        result['footer_links'] = prepare_footer_links(
            dest.full_filename, self.resources)

        result['breadcrumb'] = prepare_breadcrumb_links(key, self.resources)

        result['menu_general'] = prepare_menu_links(key, self.resources)

        return result

    ###########################################################################
    # Add a page node
    #
    # @param filename the filename of the md file to start
    # @param parent_filename the filename of the md file parent
    ###########################################################################
    def create_page(self, key, target_folder):
        if not test_node(self.resources, key, 'is_on_filesystem'):
            return None

        source = self.resources.nodes[key]['resource']
        dest = self.resources.nodes[key]['target_resource']

        if not test_node(self.resources, key, 'is_md'):
            common.check_create_folder(dest.filename_path)
            shutil.copy(source.full_filename,
                        dest.full_filename)
            return

        the_page = page.Page(source.full_filename,
                             jinja_env=self.jinja_env,
                             context=self.get_context_for_page(key,
                                                               target_folder))

        out_links = [self.resources.edges[edge]['link']
                     for edge in self.resources.out_edges(key)]
        the_page.content = mdcommon.update_links_in_md_text(
            the_page.content, out_links)

        the_page.write(dest.full_filename)

    ###########################################################################
    # the jinja2 environment
    # @return the value
    ###########################################################################
    @property
    def jinja_env(self):
        return self.__env

    ###########################################################################
    # the jinja2 environment
    # @param value The value to set
    ###########################################################################
    @jinja_env.setter
    def jinja_env(self, value):
        self.__env = value

    ###########################################################################
    # the context environment
    # @return the value
    ###########################################################################
    @property
    def context(self):
        return self.__context

    ###########################################################################
    # the folder of the first file of the web site the root page
    # @return the value
    ###########################################################################
    @property
    def source_root_path(self):
        return self.__resources.graph['source_root_path']

    ###########################################################################
    # the tree of resources
    # @return the value
    ###########################################################################
    @property
    def resources(self):
        return self.__resources

    ###########################################################################
    # the tree of resources
    # @return the value
    ###########################################################################
    @property
    def internal_dep(self):
        return self.__internal_dep

    ###########################################################################
    # __repr__ is a built-in function used to compute the "official"
    # string reputation of an object
    # __repr__ goal is to be unambiguous
    ###########################################################################
    def __repr__(self):
        return repr(self.resources)

    ###########################################################################
    # __str__ is a built-in function that computes the "informal"
    # string reputation of an object
    # __str__ goal is to be readable
    ###########################################################################
    def __str__(self):
        result = ""
        result += "source root path=%s\n" % self.source_root_path
        result += "Context:\n"
        result += str(self.context)
        result += "\n"
        count = 0
        count_max = len(self.resources)
        for node in self.resources:
            count += 1
            desc = "Error -->"
            if 'is_on_filesystem' in self.resources.nodes[node]:
                desc = "File --> "
            if 'is_link' in self.resources.nodes[node] and \
                    self.resources.nodes[node]['is_link']:
                desc = "Link --> "
            result += "%3d / %3d: %s%s\n" % (count, count_max, desc, str(node))
        return result

###############################################################################
# Create a graph for dot
#
# @return the local folder.
###############################################################################
def create_dot_graph(site):
    result = nx.DiGraph()

    for node_key in site:
        result.add_node(node_key)

    for (src, dest) in site.edges:
        result.add_edge(src, dest)

    return result

###############################################################################
# Create a graph for dot
#
# @return the local folder.
###############################################################################
def generate_site(homepage_full_path, output_folder=None, clean_output=True):
    """
    This function build an entire web site.

    @type homepage_full_path: string
    @param homepage_full_path: The name and path of the home page
                    markdown file to work with.
                    This file is supposed to be a markdown file.

    @type output_folder: string
    @param output_folder: the folder to put the web site.

    @type clean_output: boolean
    @param clean_output: clean or not clean the output folder.

    @return nothing
    """
    homepage_full_path = common.check_is_file_and_correct_path(
        homepage_full_path)

    if output_folder is None:
        input_folder = os.path.split(homepage_full_path)[0]
        output_folder = os.path.join(input_folder, "dist")

    output_folder = common.set_correct_path(output_folder)
    if clean_output and os.path.isdir(output_folder):
        shutil.rmtree(output_folder)
    output_folder = common.check_create_folder(output_folder)

    the_site = WebSite(homepage_full_path)
    the_site.create_site(output_folder)


###############################################################################
# Get the local folder of this script
#
# @return the local folder.
###############################################################################
def get_local_folder():
    return os.path.split(os.path.abspath(os.path.realpath(
        __get_this_filename())))[0]


###############################################################################
# Find the filename of this file (depend on the frozen or not)
# This function return the filename of this script.
# The function is complex for the frozen system
#
# @return the filename of THIS script.
###############################################################################
def __get_this_filename():
    result = ""

    if getattr(sys, 'frozen', False):
        # frozen
        result = sys.executable
    else:
        # unfrozen
        result = __file__

    return result


###############################################################################
# Set up the logging system
###############################################################################
def __set_logging_system():
    log_filename = os.path.splitext(os.path.abspath(
        os.path.realpath(__get_this_filename())))[0] + '.log'
    logging.basicConfig(filename=log_filename, level=logging.DEBUG,
                        format='%(asctime)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(asctime)s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)


###############################################################################
# Launch the test
###############################################################################
def __launch_test():
    import pytest
    pytest.main(__get_this_filename())


###############################################################################
# Main script call only if this script is runned directly
###############################################################################
def __main():
    # ------------------------------------
    logging.info('Started %s', __get_this_filename())
    logging.info('The Python version is %s.%s.%s',
                 sys.version_info[0], sys.version_info[1], sys.version_info[2])

    # generate_site(
    #     r"C:\dev\projet-ge.fr\informations\guichet-entreprises.fr\fr\index.md")

    num_ex = 13

    the_folder = os.path.join(get_local_folder(),
                              "../../examples/example%02d/" % num_ex)
    folder_input = os.path.join(the_folder, "input-md/")
    folder_output = os.path.join(the_folder, "output/")

    folder_input = common.check_create_folder(folder_input)
    if os.path.isdir(folder_output):
        shutil.rmtree(folder_output)
    folder_output = common.check_create_folder(folder_output)

    shutil.rmtree(folder_output)
    folder_output = common.check_create_folder(folder_output)

    print("-----------------------------")
    print("Folder input:%s" % folder_input)
    print("Folder output:%s" % folder_output)
    print("-----------------------------")

    # test_compute_url()
    xxx = WebSite(os.path.join(folder_input, "index.md"))
    xxx.create_site(folder_output)

    # # for key in xxx.resources:
    # #     print(repr(key))

    # from networkx.drawing.nx_pydot import write_dot
    # write_dot(create_dot_graph(xxx.resources),
    #           os.path.join(get_local_folder(),
    #                        '../../examples', "graph",
    #                        "web.dot"))

    # # print(xxx)

    logging.info('Finished')
    # ------------------------------------


###############################################################################
# Call main function if the script is main
# Exec only if this script is runned directly
###############################################################################
if __name__ == '__main__':
    __set_logging_system()
    __main()
