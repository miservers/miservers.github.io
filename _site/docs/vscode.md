## VS Code
- Config files:
  they are located in **.vscode** directory

## Tasks
Execute external tools(make, ant, etc)

By `Terminal-> Configure Tasks...` or directely in **tasks.json** file

To run a task: `Terminal-> Run Task`

To create a custom task : example `make clean`: 
```json
{
    "label": "JVM: Make Clean",
    "type": "shell",
    "command": "make",
    "args": [
        "clean"
    ],
    "options": {
        "cwd": "${workspaceFolder}/jvm",
        "env": {
            "NODE_ENV": "development"
        }
    }
},
```
use `options` to specify variables such as current working directory(cwd), environment, etc



## Debugging C++ in VS Code (v.1.70)
- Extensions to install: 
  - C++ extension for VS Code

Theses config files are located in **.vscode** folder.

- Configure **.vscode/launch.json**: `Run -> Add Configutaion...`

- Configure **.vscode/tasks.json**: `Terminal -> Configure Tasks...`