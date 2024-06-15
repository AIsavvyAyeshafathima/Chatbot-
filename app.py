import json
import os
from config import DefaultConfig
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext, ActivityHandler, MessageFactory
from aiohttp import web
from aiohttp.web import Request, Response
from http import HTTPStatus
from botbuilder.schema import Activity
from botbuilder.core.integration import aiohttp_error_middleware

# Initialize the Text Analytics client
CONFIG = DefaultConfig()

# 2024/14/6 - START extended for T6 project in MSAI631- sentiment analysis to the bot
credential = AzureKeyCredential(CONFIG.API_KEY)
endpointURI = CONFIG.ENDPOINT_URI
text_analytics_client = TextAnalyticsClient(endpoint=endpointURI, credential=credential)
# 2024/14/16 - STOP extended for T6 project

# Define settings for the Bot Framework Adapter
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)

# Analyze sentiment
def analyze_sentiment(client, text):
    documents = [text]
    response = client.analyze_sentiment(documents=documents)[0]
    return response.sentiment

# Bot activity handler
class SentimentEchoBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        # Get the incoming message text
        text = turn_context.activity.text

        # Analyze sentiment
        sentiment = analyze_sentiment(text_analytics_client, text)

        # Construct the response message
        response_text = f"Echo: {text}\nSentiment: {sentiment}"

        # Send the response
        await turn_context.send_activity(MessageFactory.text(response_text))

bot = SentimentEchoBot()

async def messages(req: Request) -> Response:
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    # Perform Sentiment Analysis
    # 2024/1/5 - MSAI 631 - Start Perform Sentiment Analysis Here
    textToUse = body["text"]
    print(f"textToUse = {textToUse}")
    documents = [{"id": "1", "language": "en", "text": body["text"]}]
    response = text_analytics_client.analyze_sentiment(documents)
    successful_responses = [doc for doc in response if not doc.is_error]
    # 2024/1/5 - MSAI 631 - END Perform Sentiment Analysis Here

    # Define an internal on_turn function to handle the response logic
    async def on_turn(turn_context: TurnContext):
        sentiment = analyze_sentiment(text_analytics_client, textToUse)
        response_text = f"Echo: {textToUse}\nSentiment: {sentiment}"
        await turn_context.send_activity(MessageFactory.text(response_text))

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



