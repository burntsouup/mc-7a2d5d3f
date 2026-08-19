import asyncio

import edge_tts


async def main():
    voices = await edge_tts.list_voices()
    rows = [v for v in voices if v["Locale"].startswith("en-US")
            and "Multilingual" in v["ShortName"]]
    for v in sorted(rows, key=lambda x: x["ShortName"]):
        tag = v.get("VoiceTag", {}) or {}
        pers = ", ".join(tag.get("VoicePersonalities", []) or [])
        print(f"  {v['ShortName']:<40} {v['Gender']:<7} {pers}")


asyncio.run(main())
