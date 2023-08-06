from behave import given, then

from rikki.behave.context import Context
from rikki.behave.steps.utils import http_data
from rikki.behave.steps.utils import verify_number_of_request
from rikki.mitmproxy.delegate_replace import ReplacementConfig, InterceptAndReplace


@given("Intercept and replace http data")
def step_replace_http_data(context: Context):
    http_step_data = http_data(context)

    if http_step_data:
        config = ReplacementConfig(
            filter_request=http_step_data.filter_request,
            filter_response=http_step_data.filter_response,
            replacement_request=http_step_data.replacement_request,
            replacement_response=http_step_data.replacement_response,
            wait_response=False
        )
        plugin = InterceptAndReplace(config=config, recursive=False)
        context.proxy.add_delegate(plugin)


@given("Replace http data")
def step_replace_http_data(context: Context):
    http_step_data = http_data(context)

    if http_step_data:
        config = ReplacementConfig(
            filter_request=http_step_data.filter_request,
            filter_response=http_step_data.filter_response,
            replacement_request=http_step_data.replacement_request,
            replacement_response=http_step_data.replacement_response,
        )
        plugin = InterceptAndReplace(config=config, recursive=False)
        context.proxy.add_delegate(plugin)


@then('verify {number:d} requests. With tag: "{tag}"')
def step_verify_number_of_requests(context: Context, number, tag):
    verify_number_of_request(
        context=context,
        number=number,
        tag=tag,
        second_attempt=True
    )
