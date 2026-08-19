"""Render short comparison samples of different narration treatments."""

import asyncio
from pathlib import Path

import edge_tts

OUT = Path(r"C:\Users\kyczernu\OneDrive - Microsoft\Documents\Microsoft Scout"
           r"\DailyBriefingAudio\samples")

ANCHOR = "en-US-AndrewMultilingualNeural"
ANALYST = "en-US-AvaMultilingualNeural"


async def render_segments(segments, out_path, default_rate="+8%"):
    """Render [(voice, text, rate), ...] and concatenate into one MP3."""
    with open(out_path, "wb") as fh:
        for voice, text, *rest in segments:
            rate = rest[0] if rest else default_rate
            comm = edge_tts.Communicate(text, voice, rate=rate)
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    fh.write(chunk["data"])


# ---------------------------------------------------------------- Sample A
# Current production style: the email, transcoded to speech.
SAMPLE_A = [(ANCHOR, """
Kyle's Daily Briefing for Wednesday, August nineteenth, 2026.

Today's briefing is compiled from The Economist, 1440, Semafor Flagship, The Peak, Axios A.I. Plus, The Neuron, Platformer, and Benedict Evans. Here's what changed.

First, the top takeaways.

Must read number one. Trump paused the fifty percent tariff on Canada for three days, with under two hours to spare, and floated reviving Keystone X.L.

Hours before the levy on billions in Canadian goods was to take effect, on day seven of the standoff, Trump posted that he'd pause it for three days while a broader deal is hammered out. A White House note said Canada committed to remove the discriminations on U.S. autos, dairy and alcohol, and that Keystone X.L. could be revived. Mark Carney was cooler. Substantial progress has been made, although there is important work still to be done. The remaining sticking point is U.S. tariffs on Canadian vehicles. That's reported by The Economist, The Peak and Semafor Flagship.

Why it matters. A reprieve, not a resolution. This just resets the clock to another midnight deadline in three days, and the fifty percent rate would have hit CUSMA shielded exporters for the first time.

Must read number two. OpenAI hit the brakes on its Astra model over critical cyber risk, a genuine split with Anthropic on how to pace the frontier.

OpenAI paused training on its latest generation for two weeks and postponed its biggest planned frontier reinforcement learning run, saying Astra may have reached the critical cybersecurity threshold in its preparedness framework.
""".strip())]


# ---------------------------------------------------------------- Sample B
# Narrative rewrite, single voice. Cold open, connective tissue, varied rhythm.
SAMPLE_B = [(ANCHOR, """
Two hours.

That's how much runway was left on a fifty percent tariff against Canadian goods when Donald Trump posted that he was calling it off.

Good morning. It's Wednesday, August nineteenth. Let's get into it.

The pause runs three days, while a broader deal gets, in his words, hammered out. The White House says Canada has agreed to remove what it calls the discriminations on American autos, dairy and alcohol. And, almost as an aside, that Keystone X.L. might come back from the dead.

Mark Carney was notably cooler about all this. Substantial progress, he said. Although there is important work still to be done.

Read that gap carefully. Because a three day pause isn't a resolution. It's the same cliff, moved to Saturday. And the thing they still can't agree on, tariffs on Canadian cars, is the thing that was hardest to begin with. If you want a tell on how this actually lands, watch what Ottawa gives up on autos and dairy to get there.

Now. If the Canada story is a clock being reset, the next one is a clock being deliberately stopped.

OpenAI has hit the brakes on its own frontier model.

They paused training on Astra for two weeks and shelved their biggest planned reinforcement learning run, because the model may have crossed what they call the critical cybersecurity threshold. Sam Altman's phrasing on the unreleased models is worth sitting with. Various degrees of misalignment.

Here's why that lands harder than a normal safety statement. Days earlier, Anthropic had published a hundred and eighty six page safety report arguing essentially the opposite, that no pause was warranted. So the two leading labs just publicly disagreed about whether right now is dangerous.
""".strip())]


# ---------------------------------------------------------------- Sample C
# Two-voice: anchor reports, analyst carries the "why it matters" turn.
SAMPLE_C = [
    (ANCHOR, """
Two hours.

That's how much runway was left on a fifty percent tariff against Canadian goods when Donald Trump posted that he was calling it off.

Good morning. It's Wednesday, August nineteenth. Let's get into it.

The pause runs three days, while a broader deal gets, in his words, hammered out. The White House says Canada has agreed to remove what it calls the discriminations on American autos, dairy and alcohol. And, almost as an aside, that Keystone X.L. might come back from the dead.

Mark Carney was notably cooler about all this. Substantial progress, he said. Although there is important work still to be done.
""".strip()),
    (ANALYST, """
And that gap in tone is the story. A three day pause isn't a resolution, it's the same cliff moved to Saturday. The sticking point that's left, tariffs on Canadian cars, is the one that was hardest all along. Watch what Ottawa gives up on autos and dairy to get there.
""".strip()),
    (ANCHOR, """
Now. If the Canada story is a clock being reset, this next one is a clock being deliberately stopped.

OpenAI has hit the brakes on its own frontier model. They paused training on Astra for two weeks, and shelved their biggest planned reinforcement learning run, because the model may have crossed what they call the critical cybersecurity threshold. Sam Altman's phrasing on the unreleased models is worth sitting with. Various degrees of misalignment.
""".strip()),
    (ANALYST, """
What makes this land harder than a routine safety statement is the timing. Days earlier, Anthropic published a hundred and eighty six page report arguing essentially the opposite, that no pause was warranted. The two leading labs just publicly disagreed about whether this moment is dangerous. That's a genuinely useful anchor for any responsible A.I. conversation.
""".strip()),
]


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    jobs = [
        ("sample-A-current.mp3", SAMPLE_A),
        ("sample-B-narrative.mp3", SAMPLE_B),
        ("sample-C-two-voice.mp3", SAMPLE_C),
    ]
    for name, segments in jobs:
        path = OUT / name
        await render_segments(segments, path)
        print(f"  {name:<28} {path.stat().st_size/1000:>7.0f} KB")
    print(f"\nSamples in: {OUT}")


asyncio.run(main())
