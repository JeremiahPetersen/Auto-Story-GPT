# Auto-Story-GPT
This code is a Flask web app that utilizes GPT-3.5 to generate AI responses for storytelling. It allows users to input a story idea, select a character or narrator, and generate responses based on the provided inputs. Users can also adjust for continuity or logic issues in a story, and rewrite the story to improve it.
# How to Use
You can adjust the character names / personalities in the html and json files to your specifications.  I have provided a Futurama story generator as an example use case.
You start by creating a story idea and choose a character, narrator, or scene description, and click generate.  The story will append to the bottom of the page.  You can edit the created story at any time.  You can continue the story with as many generations as you desire.

# Example Use

Start by typing an idea into the “Story Idea:” field. Then choose a character (Typically I choose “Narrator” or “Scene Description” to start the story. Then click generate. The story will be generated at the bottom of the screen. This story is fed back into ChatGPT on each call, so continuity is maintained. You can edit any part of the story being generated. There are also options to have the bot rewrite, adjust for continuity, or undo/redo.
Example Use:

Story Idea: The scene opens up with Professor Farnsworth saying “Good news everyone!”

--> Selected “Scene Description” clicked generate.

2. Story Idea: continue the story with dialog including Leela

--> Selected “Leela” clicked generate (Edited some of the story at the BOTTOM OF THE PAGE to remove unwanted sentences.)

3. Story Idea” next scene with Zoidberg

--> Selected “Zoidberg” clicked generate (...)

Don't forget to put your OPEN AI api key in the .env file
