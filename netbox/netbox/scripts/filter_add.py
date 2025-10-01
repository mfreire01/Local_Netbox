from extras.scripts import Script, ChoiceVar
from dcim.models import Site
import yaml


class SiteStatusFilter(Script):
    class Meta:
        name = "SiteStatusFilter"
        description = "Filter sites by status and show the output with YAML format"

    status = ChoiceVar(
        choices=[
        ('active', 'Active'),
        ('planned', 'Planned'),
        ],
        required=True,
        description="Select site status"
    )

    def run(self, data, commit):
        selected_status = data["status"]

        try:
            sites = Site.objects.filter(status=selected_status)
        except Exception as e:
            self.log_failure(f"Error querying: {e}")
            return "Error: could not make the query."

        if not sites.exists():
            self.log_warning(f"No sites found with status '{selected_status}'")
            return f"No sites found with status '{selected_status}'."

        log_entries = []
        for site in sites:
            log_entry = f"#{site.id}: {site.name} - {site.status}"
            self.log_info(log_entry)
            log_entries.append({
                "id": site.id,
                "name": site.name,
                "status": site.status
            })

        try:
            yaml_output = yaml.dump(log_entries, sort_keys=False)
        except yaml.YAMLError as e:
            self.log_failure(f"Error creating YAML output: {e}")
            return "Error creating YAML output"

        return yaml_output