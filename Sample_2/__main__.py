from app_claims import optional_claims
from app_permissions import default_permissions, all_permissions
from context import get_context
from app_registration import AppBuilder, AppDefinitionBuilder


context = get_context()

# Working Example

app2_def = AppDefinitionBuilder.build_composite(title='SampleApp_2', name='sample.app2', business='personal')
app2_def.add_claims(optional_claims())
app2_def.add_permissions(default_permissions())
app2 = AppBuilder.create_composite_app(app2_def, context)
