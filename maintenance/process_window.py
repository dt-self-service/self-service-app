from dynatrace.tenant import maintenance
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