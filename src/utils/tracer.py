import os
from phoenix.otel import register

# configure the Phoenix tracer
tracer_provider =  register(
        project_name=os.getenv('MODEL_PARAMS_ID'),
        endpoint="http://10.10.0.199:6006/v1/traces",
        auto_instrument=True
    )
tracer = tracer_provider.get_tracer(__name__)