import io
import json
import yaml
import shutil
import os.path
from jinja2 import Template
from importlib import import_module
from .filenode import FileNode


FOLDER_DIST = 'dist'


def _get_config(config_file):
    data = None
    with open(config_file, 'r') as stream:
        data = yaml.safe_load(stream)
    return data


def _get_template(template_path):
    if '/' not in template_path:
        template_module = import_module(template_path)
        template_path = os.path.dirname(template_module.__file__)

    html = None
    full_path = os.path.join(template_path, 'index.html')
    with open(full_path, 'r') as f:
        html = f.read()
    return Template(html)


def _create_page(file_node, page_params, page_template):
    path = file_node.get_path()
    full_path = os.path.join(FOLDER_DIST, path)

    if file_node.kind == FileNode.KIND_FILE:
        page_params['page'] = {
            'title': file_node.name,
            'content': file_node.get_html(),
            'edit_url': file_node.get_edit_url(),
        }
        with open(full_path + '.html', 'w') as f:
            f.write(page_template.render(page_params))
    elif file_node.kind == FileNode.KIND_DIRECTORY:
        if not os.path.exists(full_path):
            os.makedirs(full_path)
    else:
        raise Exception('Filetype {} is not supported'.format(file_node.kind))


def _create_navigation_html(file_node):
    children_html = ''
    title = ''

    if file_node.parent is not None and file_node.kind == FileNode.KIND_FILE:
        title = '<a href="{}">{}</a>'.format(
            file_node.get_url(), file_node.name)
    elif file_node.parent is not None and file_node.kind == FileNode.KIND_DIRECTORY:
        title = file_node.name

    if len(file_node.children) > 0:
        children_li = [
            '<li>{}</li>'.format(_create_navigation_html(child)) for child in file_node.children]
        children_html = '<ul>{}</ul>'.format(''.join(children_li))
    return '{}{}'.format(title, children_html)


def _create_content_summary(root):
    content = []
    queue = [root]
    document_id = 1

    while len(queue) > 0:
        file_node = queue.pop()
        if file_node.kind == FileNode.KIND_FILE:
            content.append({
                'id': document_id,
                'title': file_node.name,
                'content': file_node.get_text(),
                'url': file_node.get_url(),
            })
            document_id += 1
        for child in file_node.children:
            queue.append(child)

    # Write content summary
    with open(os.path.join(FOLDER_DIST, 'content.js'), 'w') as f:
        f.write('var CONTENT = ')
        json.dump(content, f)

    
def _create_page_collection(root, page_params, page_template):
    queue = [root]

    while len(queue) > 0:
        file_node = queue.pop()
        _create_page(file_node, page_params, page_template)
        for child in file_node.children:
            queue.append(child)


def generate(args):
    config = _get_config(args.config)
    page_template = _get_template(config['template'])
    page_params = {
        'site': {
            'title': config['title'],
            'navigation': '',
        },
        'page': { 
            'title': '',
            'edit_url': '',
            'content': '',
        },
    }

    # Generate folder tree
    root = FileNode(
        name='',
        kind=FileNode.KIND_DIRECTORY
    )
    for source_name in config['sources']:
        source = config['sources'][source_name]
        if 'title' not in source.keys():
            source['title'] = source_name
        
        source_module = import_module(source['type'])
        source_root = source_module.source_generate(source)
        root.add_child(source_root)
    page_params['site']['navigation'] = _create_navigation_html(root)

    # Generate files
    if os.path.exists(FOLDER_DIST):
        shutil.rmtree(FOLDER_DIST, ignore_errors=False, onerror=None)
    _create_page_collection(root, page_params, page_template)
    _create_content_summary(root)

    # Write intro page
    if 'intro' in config.keys():
        shutil.copyfile(
            os.path.join(FOLDER_DIST, config['intro']),
            os.path.join(FOLDER_DIST, 'index.html')
        )
