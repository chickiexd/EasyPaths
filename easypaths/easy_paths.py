import os

from .default_paths import DEFAULT_CONFIG


class EasyPaths:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        """Creates a new instance of the singleton class EasyPaths if one does not exist.

        Returns:
            EasyPaths: A singleton instance of the EasyPaths.
        """
        if cls._instance is None:
            cls._instance = super(EasyPaths, cls).__new__(cls)
        return cls._instance

    def __init__(self, project_dir=None):
        """Initializes the EasyPaths as a singleton class that manages paths for different users.

        Args:
            project_dir (str, optional): The absolute or relative path to the project. Defaults to None.
        Raises:
            ValueError: If `project_dir` is not provided on the first instantiation.
        """
        if not self._initialized or project_dir is not None:
            self.project_dir = project_dir
            self.user_paths = {}
            self.current_user = None
            if project_dir is not None:
                EasyPaths._initialized = True
                project_dir = project_dir.lstrip("/").rstrip("/")
                self._initialize_default_configs()
                self._set_project_dir_for_all_users(project_dir)
        else:
            raise ValueError("project_dir must be provided on the first instantiation")

    def _initialize_default_configs(self):
        """Initializes the EasyPaths with default configurations for users and their paths from default_paths.py."""
        for user_id, paths in DEFAULT_CONFIG.items():
            self.add_user(user_id, paths.get("home_dir"))

            # TODO could pop home_dir before the loop
            # paths.pop('home_dir')

            for path_key, path_value in paths.items():
                if path_value[0] == "/":
                    self.add_abs_path(path_key, path_value, user_id)
                else:
                    self.add_path(path_key, path_value, False, user_id)

    def _set_project_dir_for_all_users(self, project_dir):
        """Sets the project directory for all registered users.

        Args:
            project_dir (str): The relative project directory to set for all users.
        Raises:
            -
        """
        if os.path.isabs(project_dir):
            raise ValueError("project_dir must be a relative path.")
        for user_id in self.user_paths:
            project_dir_abs = os.path.join(
                self.user_paths[user_id]["home_dir"], project_dir
            )
            self.add_abs_path("project_dir", project_dir_abs, user_id)

    def _get_abs_path(self, path):
        """Return the absolute path of a given path.

        Args:
            path (str): The path to convert to an absolute path.
        Returns:
            str: The absolute path of the given path.
        """
        return os.path.abspath(path)

    def set_current_user(self, user_id):
        """Set the default user for subsequent operations.

        Args:
            user_id (str): The user id to set as the default user.
        Raises:
            ValueError: If the user does not exist.
            ValaeError: If the user's project directory does not exist.
        """
        if not EasyPaths._initialized:
            raise ValueError("EasyPaths is not initialized with a project dir.")
        if user_id in self.user_paths:
            self.current_user = user_id
            project_dir_path = self.get_path("project_dir")
            if not os.path.isdir(project_dir_path):
                raise ValueError(f"Users project directory does not exist.")
        else:
            raise ValueError("User does not exist.")

    def add_user(self, user_id, home_dir):
        """Add a new user to the path manager.

        Args:
            user_id (str): The user to add.
            home_dir (str): The absolute path to the home directory of the user.
        """
        if not EasyPaths._initialized:
            raise ValueError("EasyPaths is not initialized with a project dir.")
        if user_id not in self.user_paths:
            self.user_paths[user_id] = {}
            if home_dir is not None:
                self.user_paths[user_id]["home_dir"] = home_dir
                self.user_paths[user_id]["project_dir"] = os.path.join(
                    home_dir, self.project_dir
                )

    def add_path(self, path_key, path_value, user_id=None):
        """Add a path for a specific user and key.

        Args:
            path_key (str): The key to identify the path.
            path_value (str): The relative path to add.
            user_id (str): The user to add the path for. If None path added for all users
        Raises:
            ValueError: If the path value is an absolute path.
            ValueError: If the user does not exist.
        """

        def _add_path(path_key, path_value, user_id):
            path_value = os.path.join(
                self.user_paths[user_id]["project_dir"], path_value
            )
            path_value = os.path.normpath(path_value)
            self.user_paths[user_id][path_key] = path_value

        if not EasyPaths._initialized:
            raise ValueError("EasyPaths is not initialized with a project dir.")
        if os.path.isabs(path_value):
            raise ValueError("Path value must not be an absolute path.")
        if path_value == "":
            raise ValueError("Path value cannot be empty.")
        if user_id is not None and not user_id in self.user_paths:
            raise ValueError("User does not exist. Please add the user first.")

        path_value = path_value.rstrip("/")

        if user_id is not None:
            _add_path(path_key, path_value, user_id)
        else:
            for user_id in list(self.user_paths.keys()):
                _add_path(path_key, path_value, user_id)

    def add_abs_path(self, path_key, path_value, user_id=None):
        """Add an absolute path for a specific user and key.

        Args:
            path_key (str): The key to identify the path.
            path_value (str): The absolute path to add.
            user_id (str): The user to add the path for. If None path added for all users
        Raises:
            ValueError: If the path value is not an absolute path.
            ValueError: If the user does not exist.
        """

        def _add_abs_path(path_key, path_value, user_id):
            path_value = os.path.normpath(path_value)
            self.user_paths[user_id][path_key] = path_value

        if not EasyPaths._initialized:
            raise ValueError("EasyPaths is not initialized with a project dir.")
        if not os.path.isabs(path_value):
            raise ValueError("Path value must be an absolute path.")
        if user_id is not None and not user_id in self.user_paths:
            raise ValueError("User does not exist. Please add the user first.")

        if user_id is not None:
            _add_abs_path(path_key, path_value, user_id)
        else:
            for user_id in list(self.user_paths.keys()):
                _add_abs_path(path_key, path_value, user_id)

    def get_path(self, path_key, user_id=None):
        """Retrieve a path for a specific path key, optionally overriding the default user.

        Args:
            path_key (str): The key to identify the path.
            user_id (str, optional): The user to retrieve the path for. Defaults to current_user.
        Raises:
            ValueError: If no user provided and no current user set.
            ValueError: If the path key is not found for the user.
        """
        if not EasyPaths._initialized:
            raise ValueError("EasyPaths is not initialized with a project dir.")
        effective_user = user_id or self.current_user
        if effective_user is None:
            raise ValueError(
                "No user set. Please set a user first or provide a user_id."
            )
        if not (effective_user in self.user_paths):
            raise ValueError("User does not exist. Please add the user first.")
        if not path_key in self.user_paths[effective_user]:
            raise ValueError("Path key not found for user.")

        return self.user_paths[effective_user][path_key]
