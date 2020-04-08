from dynatrace.tenant import maintenance
from .forms import filter_set
import user_variables as uv

def create_filters_from_formset(input_formset, form_prefix="form"):
  """Formset processing for entity filters"""
  scope = {
    "entities": [],
    "matches": []
  }

  for entity_entry in input_formset.forms:
    if entity_entry.cleaned_data.get('filter_value') != "":

      if entity_entry.cleaned_data.get('tags_or_entities') == "TAGS":
        tag_list = []
        for tag_entry in entity_entry.cleaned_data.get('filter_value').split(';'):
          tag = maintenance.parse_tag(tag_entry)
          tag_list.append(tag)
        
        match = {
          "type": entity_entry.cleaned_data.get('entity_type'),
          "managementZoneId": "null",
          "tags": tag_list
        }
        scope['matches'].append(match)

      if entity_entry.cleaned_data.get('tags_or_entities') == "ENTITIES":
        for specific_entity in entity_entry.cleaned_data.get('filter_value').split(';'):
          scope['entities'].append(specific_entity)

  return scope

def parse_submit_form(post_args):

  day = None
  if 'window_day_of_week' in post_args and post_args['window_recurrence'] == 'WEEKLY':
      day = post_args.pop ('window_day_of_week')[0]
  if 'window_day_of_month' in post_args and post_args['window_recurrence'] == 'MONTHLY':
      day = post_args.pop ('window_day_of_month')[0]
  
  schedule = maintenance.generate_schedule (
          post_args.pop ('window_recurrence')[0],
          post_args.pop ('window_start_time')[0],
          post_args.pop ('window_duration')[0],
          post_args.pop ('window_maintenance_start')[0],
          post_args.pop ('window_maintenance_end')[0],
          day
  )

  maintenance_window_name = post_args.pop ('window_name')[0]
  maintenance_window_desc = post_args.pop ('window_description')[0]
  maintenance_window_supp = post_args.pop ('window_supression')[0]
  maintenance_window_plan = post_args.pop ('window_planned')[0]
  post_args.pop ('cluster_name')[0]
  post_args.pop ('tenant_name')[0]
  post_args.pop('csrfmiddlewaretoken')
  
  formset = filter_set(post_args)
  scope = None
  print("Formset: " + str(formset.is_valid()))
  if formset.is_valid():
      scope = create_filters_from_formset (formset)

  payload = maintenance.generate_window_json (
          maintenance_window_name,
          maintenance_window_desc,
          maintenance_window_supp,
          schedule,
          is_planned=maintenance_window_plan,
          scope=scope
  )
  return payload