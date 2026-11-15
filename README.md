# 🌙 Moonbreakers

### NASA Space Apps Challenge 2026 | Chicago

**Challenge:** [Space Mission Design Game](https://www.spaceappschallenge.org/2026/challenges/space-mission-design-game/)

**Team:** Moonbreakers

**Technology:** Python | Pygame

**GitHub Repository:** [Moonbreakers – Space Apps Challenge 2026](https://github.com/BrandonPartain13/Moonbreakers-Space-Apps-Challenge-2026--Chicago)

---

## 🚀 About Moonbreakers

Moonbreakers is an educational space mission design game being developed for the 2026 NASA Space Apps Challenge.

The project aims to introduce players to the complexities of space exploration by allowing them to design, plan, and manage their own space missions.

Players will explore how scientific objectives, engineering decisions, resource limitations, and mission risks influence the success of a space exploration mission.

By combining interactive gameplay with real-world aerospace engineering concepts, Moonbreakers aims to make space mission planning more accessible, engaging, and educational.

## 🎯 Project Objectives

Moonbreakers aims to:

- Introduce players to the fundamentals of space mission design.
- Demonstrate how engineering and scientific decisions affect mission outcomes.
- Encourage critical thinking, problem-solving, and strategic planning.
- Explore the relationships between mission objectives, spacecraft capabilities, and available resources.
- Promote interest in aerospace engineering, planetary science, and STEM education.

## 🎮 Planned Game Features

### 1. Main Menu and Player Selection

An interactive menu allowing players to begin a new mission, select their player profile, and navigate game options.

### 2. Difficulty Selection

Players will be able to choose between three difficulty levels:

- **Clear skies:** A more accessible introduction to mission design.
- **First Ascent:** A balanced experience with additional planning challenges.
- **No mercy:** A more demanding experience emphasizing engineering constraints and strategic decision-making.

### 3. Spacecraft and Mission Asset Creation

Players will plan their mission by selecting and configuring assets such as:

- Rockets and spacecraft
- Scientific instruments
- Scientists, astronauts, and mission personnel

### 4. Orbital Selection

A planned feature allowing players to select orbital configurations as part of their mission design.

### 5. Rocket Launch

A planned interactive launch sequence representing the transition from mission preparation to execution.

### 6. Mission Progression

Text-based screens and interactive buttons will guide players through mission stages, decisions, and outcomes.

### 7. Save and Load System

Players can save the current mission setup after choosing a rocket tier and load it from the main screen. The system will expand as more mission choices are added.

## 🔬 Scientific and Engineering Concepts

Moonbreakers draws inspiration from real-world space mission planning, including concepts explored through NASA educational programs.

Potential educational topics include:

**Mission Scope and Constraints**

Players learn that spacecraft missions must operate within limitations involving mass, dimensions, budgets, and available technology.

**Scientific Instrument Selection**

Players explore how instruments contribute to mission objectives and why scientific priorities matter when designing spacecraft.

**Risk Management**

Mission decisions involve evaluating uncertainty, identifying potential challenges, and considering trade-offs.

**In-Situ Resource Utilization (ISRU)**

Potential gameplay scenarios may introduce the use of locally available planetary resources, such as water ice and regolith, to support exploration.

**Mission Descoping**

Players may encounter situations requiring them to adjust their mission design while preserving essential scientific objectives.

These concepts are intended to demonstrate that successful space exploration requires collaboration across multiple scientific and engineering disciplines.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core game programming |
| Pygame | Game interface, graphics, and interaction |
| GitHub | Version control and team collaboration |
| Google Docs | Brainstorming, planning, and documentation |

## 💻 Getting Started

### Prerequisites

Install Python 3 and the Pygame library.

### Installation

1. Clone the repository:

```bash
git clone https://github.com/BrandonPartain13/Moonbreakers-Space-Apps-Challenge-2026--Chicago.git
```

2. Navigate to the project directory:

```bash
cd Moonbreakers-Space-Apps-Challenge-2026--Chicago
```

3. Install Pygame:

```bash
python -m pip install pygame
```

4. Follow the repository's launch instructions once the game's main entry point is finalized.

*Note: Moonbreakers is under development. Installation and execution instructions may change as the project evolves.*

### Current demo flow

The game flows from Main (Start or Load) through Difficulty, player count, player roles, roster, rocket price tier, Rocket Configuration, Instruments and Resources, Spacecraft Configuration, and Launch. Rocket Configuration and Instruments and Resources are currently placeholder screens with Back and Next buttons. On the spacecraft configuration screen, click a field to enter a value and hover over its label or input for a short explanation. The current form uses identical tanks and identical thrusters, with one fuel amount and thrust value per unit; a burn angle of 0 means forward along the orbit. Launch saves the mission, calls GMAT through its Python API, and displays the returned trajectory or an error.

After choosing a rocket tier, **Save** is available on that screen and every following screen. It writes the current setup and screen to `savegame.json` in the game's working directory. **Load** on the main screen restores both. The save includes difficulty, players and roles, roster, rocket tier, and the player and mission customization fields. The coin images show relative price tiers; money and numeric prices are still to be defined.

Spacecraft configuration entries are included in Save, even before the form is complete. Launch requires complete inputs and a successful save before the GMAT simulation starts. The trajectory display has an Earth view and a Moon close-up, both using XY projections of GMAT coordinates. The Moon close-up shows the spacecraft only when its three-dimensional distance is within 50,000 km; a chosen burn does not necessarily produce a lunar encounter.

## 👥 Team Collaboration

Moonbreakers is a multidisciplinary project bringing together individuals with different academic backgrounds and interests.

The project encourages collaboration across areas such as:

- Aerospace engineering
- Computer science and programming
- Planetary science
- Biology and other scientific disciplines
- Game design and interactive storytelling

Team members contribute ideas, technical knowledge, and creative approaches to developing an engaging educational experience.

## 📚 Resources and References

- [NASA Space Apps Challenge](https://www.spaceappschallenge.org/)
- [Space Mission Design Game Challenge](https://www.spaceappschallenge.org/2026/challenges/space-mission-design-game/)
- [Pygame Documentation](https://www.pygame.org/docs/)
- [NASA](https://www.nasa.gov/)
- [NASA Artemis Program](https://www.nasa.gov/humans-in-space/artemis/)

## 🌌 Our Vision

Moonbreakers aims to demonstrate that space exploration is more than launching rockets. It involves creativity, collaboration, scientific curiosity, and the ability to make difficult decisions under real-world constraints.

Through interactive mission design, we hope to inspire players to explore the possibilities of space science and engineering while developing an appreciation for the people, technologies, and decisions behind successful space missions.

---

**Developed for the 2026 NASA International Space Apps Challenge — Chicago.**

*Moonbreakers is an independent educational project created for the NASA Space Apps Challenge. It is not an official NASA mission or NASA-developed game.*
