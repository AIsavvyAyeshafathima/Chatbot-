import json
from aiohttp import web
from aiohttp.web import Request, Response, json_response
from http import HTTPStatus
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
from botbuilder.core.integration import aiohttp_error_middleware

# Define settings for the Bot Framework Adapter
SETTINGS = BotFrameworkAdapterSettings("", "")
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Listen for incoming requests on /api/messages
async def messages(req: Request) -> Response:
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    user_says = activity.text if activity.text else ""  # Handle NoneType for text
    reversed_text = user_says[::-1]  # Reverse the input string

    # Define an internal on_turn function to handle the response logic
    async def on_turn(turn_context: TurnContext):
        await turn_context.send_activity(Activity(type="message", text=reversed_text))

    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    # Process the activity and call the on_turn function
    await ADAPTER.process_activity(activity, auth_header, on_turn)

    return Response(status=HTTPStatus.OK)

# Create the aiohttp web application
APP = web.Application(middlewares=[aiohttp_error_middleware])

# Add the route to handle messages
APP.router.add_post("/api/messages", messages)

# Run the web application
if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=3978)
    except Exception as e:
        raise e

