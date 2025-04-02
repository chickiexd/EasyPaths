import os

class EasyPaths:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EasyPaths, cls).__new__(cls)
        return cls._instance

    def __init__(self, project_dir=None):
        if not self._initialized or project_dir is not None:
            self.project_dir = project_dir
            self.user_paths = {}
            self.current_user = None
            if project_dir is not None:
                EasyPaths._initialized = True
                project_dir = project_dir.lstrip("/").rstrip("/")
                self._set_project_dir_for_all_users(project_dir)

    def _set_project_dir_for_all_users(self, project_dir):
        for user_id in self.user_paths:
            project_dir_abs = os.path.join(
                self.user_paths[user_id]["home_dir"], project_dir
            )
            self.add_abs_path("project_dir", project_dir_abs, user_id)

    def _get_abs_path(self, path):
        return os.path.abspath(path)

    def set_current_user(self, user_id):
        if user_id in self.user_paths:
            self.current_user = user_id

    def add_user(self, user_id, home_dir):
        if user_id not in self.user_paths:
            self.user_paths[user_id] = {}
            if home_dir is not None:
                self.user_paths[user_id]["home_dir"] = home_dir
                self.user_paths[user_id]["project_dir"] = os.path.join(
                    home_dir, self.project_dir
                )

    def add_path(self, path_key, path_value, user_id=None):
        def _add_path(path_key, path_value, user_id):
            path_value = os.path.join(
                self.user_paths[user_id]["project_dir"], path_value
            )
            path_value = os.path.normpath(path_value)
            self.user_paths[user_id][path_key] = path_value

        path_value = path_value.rstrip("/")
        if user_id is not None:
            _add_path(path_key, path_value, user_id)
        else:
            for user_id in list(self.user_paths.keys()):
                _add_path(path_key, path_value, user_id)

    def get_path(self, path_key, user_id=None):
        effective_user = user_id or self.current_user
        return self.user_paths[effective_user][path_key]

