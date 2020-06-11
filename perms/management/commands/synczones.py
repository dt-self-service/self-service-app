from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from perms.models import ZonePerms

from framework import user_variables
from framework.dynatrace.tenant import management_zones


class Command(BaseCommand):
  help = "Sync Management Zones to Permissions"

  def add_arguments(self, parser):
    pass

  def handle(self, *args, **options):
    # Iterate through each cluster and tenant and add new permissions and removed zones missing from Dynatrace now
    for cluster_key, cluster_items in user_variables.FULL_SET.items():
      initial_permissions = Permission.objects.filter(codename__startswith=cluster_key)
      for tenant in cluster_items['tenant']:
        zone_list = management_zones.get_management_zone_list(
            cluster_items, tenant)
        for zone in zone_list:
          # TODO Document Codename Limitation (100 char length).
          permission_codename = str(cluster_key) + \
              "|" + str(tenant) + "|" + str(zone['name'])

          #Create Permissions that do not exist yet & keeping track of groups that don't exist anymore
          if not Permission.objects.filter(codename=permission_codename).exists():
            Permission.objects.create(
                codename=permission_codename,
                name=permission_codename,
                content_type=ContentType.objects.get_for_model(ZonePerms)
            )
          else:
            # Bringing back all Potentially deleted Management Zones before
            Permission.objects.filter(codename=permission_codename).update(
                codename=permission_codename,
                name=permission_codename,
                content_type=ContentType.objects.get_for_model(ZonePerms)
            )
            initial_permissions = initial_permissions.exclude(codename=permission_codename)
      for unused_permission in initial_permissions:
        # Cant Delete so adding a REMOVED tag to the name to show the MZ is no longer 
        # and permissions is moot
        Permission.objects.filter(codename=unused_permission.codename).update(
          name = unused_permission.codename + " - REMOVED"
        )
