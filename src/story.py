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
        "journal_5", "analysis_results",
    ),
    "analysis_success": (
        "Analysis successful",
        (("Boss", "The crew has interpreted enough of the mission data to identify a pattern. We can now discuss what it means for the Moon."),),
        "analysis_results", "final_dialogue",
    ),
    "analysis_failure": (
        "Analysis unsuccessful",
        (("Boss", "The crew could not interpret enough of the mission data. Without a reliable analysis, we cannot determine what is damaging the Moon."),),
        "analysis_results", "game_over",
    ),
    "game_over": (
        "Game Over",
        (
            ("Boss", "These results don't look very good... I don't think the current team composition is the best idea."),
            ("You", "I sincerely apologize. What can I improve?"),
            ("Boss", "Well, our flyby didn't collect much data, and what data we did collect wasn't very helpful to finding out the reason for these craters. It's looking like we'll have to plan more than just one or two more missions for this. I must say, I am not very satisfied with the way this turned out."),
            ("You", "But we simply don't have time for more than that. I don't even know what to do."),
            ("Boss", "Well, better think of something quick! There's too much at work that we can't see."),
            ("Scene", "You leave and head to your car, but before you can turn the key in the ignition, a bright light engulfs you. All that's left of half of Earth is a large, jagged crater. The other half melts as Earth's molten layers are exposed and the atmosphere is disrupted."),
        ),
        "analysis_failure", "game_over_final",
    ),
    "final_dialogue": (
        "To the drawing board",
        (
            ("Boss", "This means that there's something outside our view, something that we can't see even from the ship we sent, that is causing this immense damage to the Moon."),
            ("You", "And we're sure that it isn't the insane amount of debris floating in our atmosphere from all our satellites and previous missions?"),
            ("Boss", "Yes, we are sure that it is NOT from the satellite debris."),
            ("You", "So there must be some sort of external factor causing this..."),
            ("Boss", "We will have to plan another mission before the Moon meets its end, leading to our demise. To the drawing board we go!"),
        ),
        "analysis_success", "to_be_continued",
    ),
}


JOURNAL_ENTRIES = (
    (
        "Dear Earth,",
        "I believe I am doing the right thing here. But one day, the people may not look upon it too favorably. I hope that the decisions we make here save the world from a slow and terribly painful end.",
        "",
    ),
    (
        "Mission control,",
        "If you saw what we were seeing, you'd be just as shocked. Our results should speak for themselves, but the impact craters are very deep and impossibly jagged, like something took a piece out of the moon, instead of an impact. I can only imagine what the reaction will be like.",
        "Captain",
    ),
    (
        "HII MISSION CONTROL!",
        "I can't believe we are really seeing these huge things up in space ourselves! We were really chosen for this job? These craters are HUGE. No wonder there's such an effect back down on Earth!!!! I really hope we can figure out why these things are happening... I know we haven't been the kindest to Earth, but it is our home and we must do our best to protect it. See you again soon!!!",
        "",
    ),
    (
        "Control,",
        "I see that we have been very successful with the first flyby. I wish to be a part of the next mission as well, since I find this very fascinating. My background as a medical doctor would greatly benefit the crew. Additionally, as I am trained in astrobiology, I find that the events happening on the lunar surface that are affecting the Earth are simply mind-boggling. I would like to continue my research in relation to these events and determine whether there is anything we can learn about these craters to solve these issues.",
        "Much appreciated,",
    ),
    (
        "Control,",
        "I find it very concerning that our first mission is simply a flyby. Like my crewmate, I wish to be a part of future missions, as my research pertains to the specific impacts that look jagged. It has impacted the geography and terrain of the moon, leading to our current research being almost useless. These are unprecedented times, and I value humankind and its contributions. I'm updating my rock collection as we speak!",
        "Signing off,\nThe Astronaut",
    ),
)
