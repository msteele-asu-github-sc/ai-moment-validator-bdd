import json
from behave import given, when, then
from pydantic import BaseModel, Field, field_validator


# =====================================================================
# AWS AI PIPELINE DATA CONTRACT (Pydantic Schema Blueprint)
# =====================================================================
class MomentSchema(BaseModel):
    moment_id: str
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence must be between 0.0 and 1.0")
    start_time: float
    end_time: float

    @field_validator('end_time')
    @classmethod
    def check_timestamps(cls, v: float, info) -> float:
        if 'start_time' in info.data and v <= info.data['start_time']:
            raise ValueError('end_time must be strictly greater than start_time')
        return v


# =====================================================================
# GHERKIN BEHAVE STEP IMPLEMENTATION
# =====================================================================

@given('an AI moment payload with ID "{moment_id}" and confidence {confidence:f}')
def step_given_payload(context, moment_id, confidence):
    context.payload_dict = {
        "moment_id": moment_id,
        "confidence": confidence
    }
    context.cloudwatch_logs = []


@given('a valid video window from {start:f} to {end:f} seconds')
def step_given_window(context, start, end):
    context.payload_dict["start_time"] = start
    context.payload_dict["end_time"] = end


@when('the QA validation harness parses the payload')
def step_when_validate(context):
    try:
        # Convert dictionary to JSON string to simulate an S3 cloud payload string
        json_payload_str = json.dumps(context.payload_dict)

        # Enforce validation using Pydantic
        MomentSchema.model_validate_json(json_payload_str)

        context.test_status = "PASSED"
        context.cloudwatch_logs.append("INFO: Metric pushed - AI Data Contract Verified")
    except Exception as e:
        context.test_status = "FAILED"
        context.error_message = str(e)
        context.cloudwatch_logs.append("WARN: Schema Validation Defect Logged")


@then('the validation check must pass successfully')
def step_then_must_pass(context):
    assert context.test_status == "PASSED", f"Expected verification pass, but execution failed."


@then('the validation check must fail')
def step_then_must_fail(context):
    assert context.test_status == "FAILED", f"Expected validation failure, but verification passed."


@then('an informational metric is routed to the CloudWatch log stack')
def step_then_check_success_log(context):
    has_info_log = any("INFO" in log for log in context.cloudwatch_logs)
    assert has_info_log is True, "Expected INFO metric entry missing from log stack."


@then('a schema validation defect notification is recorded')
def step_then_check_fail_log(context):
    has_warn_log = any("WARN" in log for log in context.cloudwatch_logs)
    assert has_warn_log is True, "Expected WARN tracking notification entry missing from log stack."
