from pulumi import export
import logging

from .app_registration import create_composite_app, CompositeAppDefinition

logger = logging.getLogger()

app_def = CompositeAppDefinition(title='Sample App', name='dm', business='bl')
app = create_composite_app(app_def)

export("app", app)