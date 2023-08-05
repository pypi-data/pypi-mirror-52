import git_profiles.utils.messages as msg
from git_profiles.commands.base_command import BaseCommand


class ShowProfile(BaseCommand):
    def execute(self) -> None:
        """Show the details of the given profile name, if it exists."""
        profile_name = self.args.profile[0]
        if not self.git_manager.check_profile_exist(profile_name):
            if not self.quiet:
                print(msg.ERR_NO_PROFILE.format(profile_name))
            return

        # Get the details of the profile
        full_name = "profile.{0}".format(profile_name)
        profile = self.git_manager.get_profile(full_name)

        print(profile_name)
        print(profile)
