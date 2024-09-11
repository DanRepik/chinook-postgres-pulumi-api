import pytest

api_id: str = None
@pytest.fixture
def gateway_endpoint():
    global api_id
    if not api_id:
        from pulumi import automation as auto

        stack = auto.select_stack(
            stack_name="local",
            work_dir=".",
        )

        stack.refresh(on_output=print)
        outputs = stack.outputs()

        api_id = outputs["gateway-api"].value if "gateway-api" in outputs else None
    return (
        f"http://{api_id}.execute-api.localhost.localstack.cloud:4566/chinook_postgres"
    )
