from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType

# Zone Perms for each app
from maintenance.models import ZonePerms as maintenance_zone_perms

import user_variables
from dynatrace.tenant import management_zones


class Command(BaseCommand):
  help = "Sync Management Zones to Permissions"

  def handle(self, *args, **options):
    # Iterate through each cluster and tenant and add new permissions and removed zones missing from Dynatrace now
    for cluster_key, cluster_items in user_variables.FULL_SET.items():
      content_type = ContentType.objects.get_for_model(maintenance_zone_perms)
      initial_permissions = Permission.objects.filter(
          codename__startswith=cluster_key, content_type=content_type)
      for tenant in cluster_items['tenant']:
        zone_list = management_zones.get_management_zone_list(
            cluster_items, tenant
        )
        for zone in zone_list:
          # TODO Document Codename Limitation (100 char length).
          permission_codename = str(cluster_key) + \
              "|" + str(tenant) + "|" + str(zone['name'])

          # Create Permissions that do not exist yet & keeping track of groups that don't exist anymore
          if not (current_permission := Permission.objects.filter(codename=permission_codename, content_type=content_type)).exists():
            Permission.objects.create(
                codename=permission_codename,
                name=permission_codename,
                content_type=ContentType.objects.get_for_model(
                    maintenance_zone_perms)
            )
          else:
            # Bringing back all Potentially deleted Management Zones before
            current_permission.update(
                codename=permission_codename,
                name=permission_codename,
                content_type=ContentType.objects.get_for_model(
                    maintenance_zone_perms)
            )
          initial_permissions = initial_permissions.exclude(
              codename=permission_codename, content_type=content_type)
      for unused_permission in initial_permissions:
        # Cant Delete so adding a REMOVED tag to the name to show the MZ is no longer
        # and permissions is moot
        Permission.objects.filter(
            codename=unused_permission.codename,
            content_type=ContentType.objects.get_for_model(
                maintenance_zone_perms)
        ).update(
            name="REMOVED - " + unused_permission.codename
        )
