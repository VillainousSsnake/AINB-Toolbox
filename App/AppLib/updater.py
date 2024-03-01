# Contains Updater class

# Importing libraries and modules
from github import Github


# Creating global vars
UpdateTagInt = 3


class Updater:

    @staticmethod
    def is_latest_update():

        github_controller = Github(None)
        repo = github_controller.get_repo("VillainousSsnake/AINB-Toolbox")
        release_tags = repo.get_releases().totalCount

        if UpdateTagInt < release_tags:
            return False

        return True
