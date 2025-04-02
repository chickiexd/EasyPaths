# EasyPaths

`EasyPaths` is a Python singleton class that streamlines the management of file and directory paths across different users within a project. It ensures each user has a consistent and customizable path setup based on either default configurations or user-defined settings. This utility is particularly valuable in environments where the current working directory (cwd) may be unreliable or inconsistent—helping maintain stable access to essential paths regardless of how or where the application is run.

## Features

- **Singleton Design:** Guarantees a single, centralized instance of the path manager across the entire application.
- **Dynamic User Handling:** Enables flexible addition and management of directory paths tailored to individual users.
- **Automated Path Setup:** Initializes default directories and paths automatically when a new user is added.
- **Active User Context:** Lets you define a current user, making their paths the default reference for future operations.
- **Flexible Path Support:** Accommodates both absolute and relative paths to suit diverse application requirements.

## Installation

Install with _pip_:

```
pip install git+ssh://git@github.com/chickiexd/EasyPaths.git
```

## Usage

Here is a basic guide on how to use `EasyPaths` in your project:

### Initialization

First, ensure that the `EasyPaths` is imported and initialized with the name of the project directory:

```python
from easypaths import EasyPaths

# Initialize with a specific project directory
path_manager = EasyPaths(project_dir='project')
```

### User Management

Add users to the path manager and set up their default paths. The user's home dir should be the absolute path to the root directory where all the projects are stored:

```python
path_manager.add_user('user1', 'user1_home_dir')
path_manager.add_user('user2', 'user2_home_dir')
```

Set the current user so that get_path calls will return the current user's paths:

```python
path_manager.set_current_user('user1')
```

### Path Configuration

Add paths for the current user or any other user:

```python
# Add a path for the specific user
path_manager.add_path('path_key', 'relative_path_value', 'user')
path_manager.add_abs_path('path_key', 'absolute_path_value', 'user')
# Add a path for all users
path_manager.add_path('path_key', 'relative_path_value')
path_manager.add_abs_path('path_key', 'absolute_path_value')
```

Get Path by key:

```python
# Get the path for the current user
path = path_manager.get_path('path_key')
# Get the path for a specific user
path = path_manager.get_path('path_key', 'user2')
```

### Example

I just initialize the 'EasyPaths' once and set the current user via a command line argument. Then I can access the paths of the current user in the whole project and dont need to adjust the paths for different users.

```python
#main.py
import argparse
from easypaths import EasyPaths

parser = argparse.ArgumentParser(description="Crnt Project")
parser.add_argument("--username", help="Username of the current user.", type=str)
parser.add_argument("--gpu_id", help="GPU IDs to use.", type=str)
args = parser.parse_args()

if args.username:
    current_user = args.username
else:
    current_user = "chickie"

# Initialize the path manager
pm = EasyPaths("example_project")

# Provide all needed paths for the project
pm.add_path("dataset", "data/dataset", "chickie")
pm.add_path("model", "models", "chickie")
pm.add_path("dataset", "other_data/dataset", "other_user")
pm.add_path("model", "models", "other_user")

# Set the current user
pm.set_current_user(current_user)
```

```python
#module.py
from easypaths import EasyPaths

pm = EasyPaths()
dataset_path = pm.get_path("dataset")
```

## TODO

- [ ] Add more checks if dirs exist
- [ ] Add more tests
