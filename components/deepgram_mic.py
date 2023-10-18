import os
import asyncio
import json
import pyaudio
import websockets

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 8000
audio_queue = asyncio.Queue()


# Used for microphone streaming only.
def mic_callback(input_data, frame_count, time_info, status_flag):
    audio_queue.put_nowait(input_data)
    return (input_data, pyaudio.paContinue)


async def run(key):
    deepgram_url = f"wss://api.deepgram.com/v1/listen?punctuate=true&encoding=linear16&sample_rate=16000"

    async with websockets.connect(
        deepgram_url, extra_headers={"Authorization": "Token {}".format(key)}
    ) as ws:

        async def sender(ws):
            try:
                while True:
                    mic_data = await audio_queue.get()
                    await ws.send(mic_data)
            except websockets.exceptions.ConnectionClosedOK:
                await ws.send(json.dumps({"type": "CloseStream"}))

        async def receiver(ws):
            async for msg in ws:
                res = json.loads(msg)
                if res.get("is_final"):
                    transcript = (
                        res.get("channel", {})
                        .get("alternatives", [{}])[0]
                        .get("transcript", "")
                    )
                    print(transcript)

        async def microphone():
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=mic_callback,
            )

            stream.start_stream()
            while stream.is_active():
                await asyncio.sleep(0.1)

            stream.stop_stream()
            stream.close()

        functions = [
            asyncio.ensure_future(sender(ws)),
            asyncio.ensure_future(receiver(ws)),
            asyncio.ensure_future(microphone()),
        ]

        await asyncio.gather(*functions)


def main():
    # DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
    DEEPGRAM_API_KEY = "967c5ce3f89d5cbb8c74107737ba36b9e1a5ba20"
    if DEEPGRAM_API_KEY is None:
        print("Please set the DEEPGRAM_API_KEY environment variable.")
        return

    asyncio.run(run(DEEPGRAM_API_KEY))


if __name__ == "__main__":
    main()
