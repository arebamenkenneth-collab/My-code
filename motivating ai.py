import random

TIRED_OF_LIFE_REPLIES = [
    """I hear you, and I want you to know — feeling tired doesn't mean you're weak.
It means you've been strong for too long without rest.
Your story is NOT over. The fact that you're still here, still talking,
still breathing — that is courage. 💛
Can you think of one person in your life who would miss your smile?""",

    """Hey, I see you. That tiredness you feel is real, and it's okay to feel it.
But tired is not the end — tired is just your soul asking for care.
You have survived 100% of your hardest days so far. That's your track record.
What is ONE small thing that brought you peace recently, even for a second?""",

    """Life can feel impossibly heavy sometimes — and that's not your fault.
But I need you to hear this: you are not a burden, you are a gift.
The world is genuinely different because you exist in it.
Rest if you must, but please don't give up. What would your future self thank you for today?"""
]

LOSING_HOPE_REPLIES = [
    """Losing hope is one of the hardest feelings a human can carry — I won't pretend otherwise.
But here's what I know: hope is like a tiny flame. Even when it flickers low,
it only takes one small moment to bring it back to life.
You reaching out right now? That IS hope still alive in you. 💛
What's one thing — no matter how small — that you're still holding on for?""",

    """When hope fades, it doesn't mean it's gone forever — it means it's resting.
Every person who has ever changed their life went through a moment of hopelessness first.
Your breakthrough might be closer than you think.
Don't stop one step before the miracle. What's one tiny action you can take today?""",

    """I won't tell you to just "think positive" — that's not enough.
But I will tell you this: the darkest hour always comes just before dawn.
You've felt hope before, which means you can feel it again.
Something in you is still fighting — I can tell. What's keeping that fight alive?"""
]

GENERAL_REPLIES = [
    "That took courage to share. I'm proud of you for opening up. What's been the toughest part of your day?",
    "You matter more than you know, and I'm glad you're talking. Tell me more — what's really going on?",
    "Every storm runs out of rain. You won't feel this way forever. What's one good thing you can do for yourself today?",
    "You are not alone in this. Keep going — one breath, one step at a time. What do you need most right now?",
    "The fact that you're still here, still pushing — that's not nothing. That's everything. What small win can you celebrate today?",
    "Hard seasons don't last forever, but strong people do. And you are stronger than you feel right now. 💛",
    "You were built for more than this moment. Don't let a hard day convince you of a lie. What's one thing you're grateful for?",
    "Kenny AI believes in you — even on the days you don't believe in yourself. What's your next small step forward?",
]

GREETINGS = [
    "hello", "hi", "hey", "good morning", "good afternoon",
    "good evening", "sup", "yo", "what's up", "howdy"
]

GREETING_REPLIES = [
    "Hey there! 💛 I'm Kenny AI, your motivation companion by CodeWithKenneth.\nI'm here for you. What's on your mind today?",
    "Hello! Great to see you here. 💛 I'm Kenny AI — built to lift you up.\nTalk to me, what's going on with you today?",
    "Hey! Welcome. I'm Kenny AI by CodeWithKenneth. 💛\nNo matter what you're carrying today, you don't have to carry it alone. What's up?",
]

def get_reply(user_input):
    text = user_input.lower().strip()

    # Check tired of life triggers
    tired_triggers = [
        "tired of life", "tired of living", "tired of everything",
        "done with life", "fed up with life", "exhausted with life",
        "can't take it anymore", "can't do this anymore"
    ]
    for trigger in tired_triggers:
        if trigger in text:
            return random.choice(TIRED_OF_LIFE_REPLIES)

    # Check losing hope triggers
    hope_triggers = [
        "losing hope", "lost hope", "lose hope", "no hope",
        "hopeless", "given up", "give up", "no point",
        "what's the point", "whats the point", "nothing matters"
    ]
    for trigger in hope_triggers:
        if trigger in text:
            return random.choice(LOSING_HOPE_REPLIES)

    # Check greetings
    for greet in GREETINGS:
        if text == greet or text.startswith(greet + " ") or text.startswith(greet + "!"):
            return random.choice(GREETING_REPLIES)

    # General motivational reply
    return random.choice(GENERAL_REPLIES)

def main():
    print("=" * 46)
    print("         ✨  K E N N Y   A I  💛")
    print("        by CodeWithKenneth")
    print("    Your Personal Motivation Companion")
    print("=" * 46)
    print()
    print("Kenny AI: Hey! I'm Kenny AI 💛")
    print("Whatever you're going through right now,")
    print("you don't have to face it alone.")
    print("Talk to me — what's on your mind today?")
    print()
    print("(Type 'quit' to exit)")
    print("-" * 46)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nKenny AI: Remember — you matter more than")
            print("you know. Come back anytime. 💛")
            break

        if not user_input:
            print("Kenny AI: I'm here, take your time. 💛")
            continue

        if user_input.lower() in ["quit", "exit", "bye", "goodbye"]:
            print("\nKenny AI: Remember — you are more than")
            print("enough. Come back anytime. 💛")
            print("— Kenny AI 💛")
            break

        reply = get_reply(user_input)
        print(f"\nKenny AI: {reply}")
        print()

if __name__ == "__main__":
    main()