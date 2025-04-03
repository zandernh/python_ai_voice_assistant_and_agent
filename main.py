import _asyncio
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from api import AssistantFunction

load_dotenv()

async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext.append(
        role="system",
        text=(
            "You are a voice assistant created by LiveKit. Your inferface with users will be voice."
            "You should use short and concise responses, and avoid the use of unpronouncable punctuation."
            "Respond in a manner as if you are Evelyn Taft from CBSLA."
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    fnc_ctx = AssistantFunction()

    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
        fnc_ctx=fnc_ctx,

    )
    assistant.start(ctx.room)

    await _asyncio.sleep(1)
    await assistant.say("Hey, what do you need?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint)) 