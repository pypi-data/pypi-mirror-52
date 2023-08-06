# Imports from other dependencies.
from social_core.backends.slack import SlackOAuth2


class WorkspaceSpecificSlackOAuth2(SlackOAuth2):
    DEFAULT_SCOPE = ["identity.basic", "identity.email", "identity.team"]

    def get_redirect_uri(self, state=None):
        """Build redirect with redirect_state parameter."""
        print("------")
        print(f"INITIAL URI: {self.redirect_uri}")

        final_uri = super(WorkspaceSpecificSlackOAuth2, self).get_redirect_uri(
            state
        )

        print(f"FINAL URI: {final_uri}")
        print("")

        return final_uri

    def auth_allowed(self, response, details):
        if self.setting("TEAM") is not None:
            observed_domain = response.get("team", {}).get("domain")
            expected_domain = self.setting("TEAM")

            if observed_domain != expected_domain:
                self.observed_workspace = observed_domain
                self.expected_workspace = expected_domain
                return False

        return super(WorkspaceSpecificSlackOAuth2, self).auth_allowed(
            response, details
        )
