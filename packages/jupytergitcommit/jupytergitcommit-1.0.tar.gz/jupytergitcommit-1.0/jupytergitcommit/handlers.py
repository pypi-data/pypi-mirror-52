import os
import json
import urllib
from github import Github
from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler


class GitCommitHandler(IPythonHandler):

    def error_and_return(self, dirname, reason):

        # send error
        self.send_error(500, reason=reason)

        # return to directory
        os.chdir(dirname)

    def put(self):

        # git vars
        g = Github(os.getenv("GIT_TOKEN"))
        branch = os.getenv("GIT_BRANCH_NAME")
        repo_name = os.getenv("GIT_REPO")
        print("Sending git commit")
        if branch:
            repo_branch = repo_name + "/" + branch
            repo = g.get_repo(repo_branch)
        else:
            repo = g.get_repo(repo_name)
        contents = repo.get_content("")

        # obtain filename and msg for commit
        data = json.loads(self.request.body.decode('utf-8'))
        filename = urllib.parse.unquote(data['filename'])
        msg = data['msg']
        print("commit message: ", msg)
        self.process_commit(g, contents, repo, filename, msg, branch)

    def process_commit(self, g, contents, repo, new_file, msg, branch):
        print("Processing git commit")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                if new_file == file_content.path:
                    self.update_file(g, msg, new_file, branch)
                else:
                    self.create_file(g, msg, new_file, branch)

    @staticmethod
    def update_file(g, msg, new_file, branch):
        g.update_file(new_file, msg, branch=branch)

    @staticmethod
    def create_file(g, msg, new_file, branch):
        g.create_file(new_file, msg, branch=branch)


def setup_handlers(nbapp):
    route_pattern = ujoin(nbapp.settings['base_url'], '/git/commit')
    nbapp.add_handlers('.*', [(route_pattern, GitCommitHandler)])
