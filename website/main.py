import os, yaml

from flask import Blueprint, render_template

main = Blueprint('main', __name__)

def get_tools():
    TOOLS_DIRECTORY = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'tools')
    tools_list = []

    class Tool():
        name: str
        content: str

    for tool in os.listdir(TOOLS_DIRECTORY):
        new_tool = Tool()
        TOOL_DIRECTORY = os.path.join(TOOLS_DIRECTORY, tool)
        CONFIG_FILE = os.path.join(TOOL_DIRECTORY, 'config.yaml')

        with open(CONFIG_FILE, 'r') as f:
            data = yaml.safe_load(f)

            name = data.get('tool_name')
            hash = data.get('hash')
            TOOL_CONTENT = os.path.join(TOOL_DIRECTORY, data.get('content'))

            new_tool.name = name
            new_tool.hash = hash
            new_tool.content = TOOL_CONTENT
        tools_list.append(new_tool)
    return tools_list

@main.route('/')
def index():
    return render_template('index.html', tools=get_tools())

