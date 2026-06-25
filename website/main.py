import os, yaml

from flask import Blueprint, render_template, send_from_directory

main = Blueprint('main', __name__)

TOOLS_DIRECTORY = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'tools')

def get_tools():
    tools_list = []
    print(TOOLS_DIRECTORY)

    class Tool():
        name: str
        hash: str
        content: str

    for tool in os.listdir(TOOLS_DIRECTORY):
        new_tool = Tool()
        TOOL_DIRECTORY = os.path.join(TOOLS_DIRECTORY, tool)
        CONFIG_FILE = os.path.join(TOOL_DIRECTORY, 'config.yaml')
        print(f'Config File {CONFIG_FILE}')

        with open(CONFIG_FILE, 'r') as f:
            data = yaml.safe_load(f)

            name = data.get('tool_name')
            hash = data.get('hash')
            TOOL_CONTENT = data.get('content')

            new_tool.name = name
            new_tool.hash = hash
            new_tool.content = TOOL_CONTENT
        tools_list.append(new_tool)
    return tools_list

@main.route('/tools/<tool_name>/<path:filename>')
def tool_files(tool_name, filename):
    print(f'File path: {os.path.join(TOOLS_DIRECTORY, tool_name, filename)}')
    return send_from_directory(os.path.join(TOOLS_DIRECTORY, tool_name), filename)

@main.route('/')
def index():
    return render_template('index.html', tools=get_tools())

