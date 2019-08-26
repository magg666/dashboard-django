from django.forms import ModelForm, ValidationError
from .models import Repository


class RepositoryForm(ModelForm):
    """ Form for adding data about user's (CodeCool student) work in Team Work Weeks
    User must add:
    url: str
        link to repository for active project on GitHub in format "https://github.com/OWNER/PROJECT_NAME"
    plan: str
        link to plan for this project TW week
    module: str
        user chooses appropriate module from four options (See model 'Repository')

    Methods:
        clean_url

    """

    class Meta:

        model = Repository
        fields = ['url', 'plan', 'module']

    def clean_url(self):
        """ Method to validate link to GitHub repository. It checks domain and necessary content
        :raise
            Validation Error
        :return:
            data: dict - processed and validated data from form
        """
        # link to repository is splitted to list:
        #   first split by '//' = [https, github.com/OWNER/PROJECT_NAME]
        #   second split by '/' = [github.com, OWNER, PROJECT]

        url_without_schema_index = 1
        domain_index = 0
        github_domain = "github.com"
        data = self.cleaned_data['url']

        if str(data).split("//")[url_without_schema_index].split("/")[domain_index] != github_domain:
            raise ValidationError("Repository url must be from GitHub")

        if len(str(data).split("//")[url_without_schema_index].split("/")) < 3:
            raise ValidationError(
                "Link to repository must contain github.com domain, name of owner and repository name separated by '/'")

        return data
