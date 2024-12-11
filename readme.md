# Template Factory

A modern GUI application for creating new projects from predefined templates. Built with Python and CustomTkinter, Template Factory provides an easy way to scaffold new projects with your preferred structure and boilerplate code.

## Features

- Template selection from dropdown menu
- Detailed template information display
- Support for nested directory structures
- Real-time template preview
- Cross-platform compatibility

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/template-factory.git
cd template-factory
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

2. Click "Load Templates" and select your `templates.json` file
3. Select a template from the dropdown
4. Enter your project name
5. Click "Create Project" to generate your project structure

## Template Configuration

Templates are defined in a `templates.json` file. Here's an example structure:

```json
[
    {
        "templateName": "Flask",
        "templateDescription": "Create a new project from a Flask template",
        "TemplateFiles": [
            {
                "name": "main.py",
                "content": "from flask import Flask\n\napp = Flask(__name__)\n\nif __name__ == '__main__':\n    app.run(debug=True)\n"
            },
            {
                "name": "templates/index.html",
                "content": ""
            }
        ]
    }
]
```

### Template Properties

- `templateName`: Name of the template (displayed in dropdown)
- `templateDescription`: Description of what the template creates
- `TemplateFiles`: Array of files to create
  - `name`: File path (supports nested directories)
  - `content`: File content as string


## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.