"""Narrative windows from Story window.txt, in story order."""

STORY_WINDOWS = {
    "opening_call": (
        "A call from mission control",
        (
            ("Voice", "Hello, is this you?"),
            ("You", "Yes, who is this?"),
            ("Voice", "We understand that you are aware of the recent events involving the new impact craters on the Moon, correct?"),
            ("You", "Yes ma'am, it's my job to know about changes in our immediate astronomical vicinity. May I ask what this is about?"),
            ("Voice", "I have a job for you. A once in a lifetime opportunity, and paid extremely well. Are you in?"),
            ("You", "Yes! I just have a few questions first..."),
        ),
        "rover_intro", "invite_team",
    ),
    "invite_team": ("Invite your Team", (), "opening_call", "menu"),
    "doubt": ("What if I'm not cut out for the mission?", (), "roles", "difficulty"),
    "who_team": ("Who's on my team?", (), "difficulty", "roster"),
    "secure_location": (
        "A secure location",
        (("Voice", "The rest will have to be done in a secure location. Please be prepared to get your security classification changed."),),
        "roster", "boss_briefing",
    ),
    "boss_briefing": (
        "Project Moonbreaker",
        (("Boss", "As you know, there have been a lot of odd things going on with our Moon recently. Our meteorologists have noticed a lot of odd weather patterns and tidal patterns. We wanted to ask you to take a look at the impact craters that keep mysteriously appearing on the lunar surface."),),
        "secure_location", "mission_offer",
    ),
    "mission_offer": (
        "The mission offer",
        (
            ("You", "Yes, I am quite aware!"),
            ("Scene", "Look at the graphs and the monitor showing recent changes in the lunar surface, as observed by satellite. A small sparkle marks the changes. The graphs show fluctuations in sea level and tidal wave speed."),
            ("You", "Ma'am, in my whole life, I have never seen or heard of such a phenomenon! Right there, I see that there is a huge increase in the gravitational pull while the mass of the Moon is decreasing! I have a theory that something is at play here which we cannot even begin to comprehend!"),
            ("Boss", "Exactly, our team is currently working on trying to decipher what this means for Earth and how it will affect current and future missions going to space. We want you to lead this team and save Earth from the disastrous possibilities as a result of these issues. Do you accept this mission?"),
        ),
        "boss_briefing", "mission_choice",
    ),
    "mission_plan": (
        "Your mission",
        (("Boss", "Here is a list of the things you will have to take care of as the leader of this mission. The mission is called Project Moonbreaker. We want you to handle designing the rocket, picking all of the instrumentation to go on the mission, and the team going on the mission."),),
        "mission_choice", "rocket_builder",
    ),
    "instrument_prompt": (
        "Choose the instruments",
        (("Boss", "Interesting choice! Hopefully our mission can be carried out with this rocket. What about the instrumentation? What would you like to take on board with you?"),),
        "rocket_configuration", "instrumentation",
    ),
    "test_prompt": (
        "Time to test the mission",
        (("Boss", "Excellent! Your team looks great! Now it's time to test out how the mission will proceed."),),
        "spacecraft_setup", "launch",
    ),
    "results_prompt": (
        "The results",
        (("Boss", "These results are very interesting. I'm not entirely sure what to make of them yet. Let's send this out to our team to get some answers."),),
        "trajectory", "data_analysis",
    ),
    "data_analysis": ("", (), "results_prompt", "final_dialogue"),
    "final_dialogue": (
        "To the drawing board",
        (
            ("Boss", "This means that there's something outside our view, something that we can't see even from the ship we sent, that is causing this immense damage to the Moon."),
            ("You", "And we're sure that it isn't the insane amount of debris floating in our atmosphere from all our satellites and previous missions?"),
            ("Boss", "Yes, we are sure that it is NOT from the satellite debris."),
            ("You", "So there must be some sort of external factor causing this..."),
            ("Boss", "We will have to plan another mission before the Moon meets its end, leading to our demise. To the drawing board we go!"),
        ),
        "data_analysis", "main",
    ),
}
