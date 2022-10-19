# DesignThinkingToolset
An application for automatically discovering post-it notes in an image, extracting text (printed or hand-written), and outputting the results as a PowerPoint presentation.

## Background
Data science and software development projects usually involve a substantial amount of user interaction. This often involves lots of post-it notes with ideas for improvements
to the current process - in Design Thinking and other User-Centred Design processes, there can be hundreds of ideas, each on a single post-it note.

These approaches are brilliant for engaging with users; but at some point, someone has to work through all these ideas and transcribe what was written. This can be very
time-consuming, is prone to error, and generally a job everybody wants to avoid.

This web app aims to make that job a bit easier.

## What the project does
This project does the following:
- Uses computer vision techniques to identify post-it notes in an image (using Azure ML services)
- Identifies and extracts text from within the image, and groups related words together
- Outputs the results as a PowerPoint (with the text overlaid on the original image), for onward processing
- Provides a web app wrapper so that a user can upload an image for processing; work through the stages above; and download the output file

The web app is currently hosted on Heroku, at http://snip-app.herokuapp.com/  However, it's hosted on a free dyno and Heroku is ending its free service, so this may 
change in the near future.  

More generally, the project is aimed at generating a better understanding of areas that I'm interested in, including:
- Developing and deploying web apps, using at least some best practice;
- Creating and using Azure services for AI / ML;
- CI / CD processes, with GitHub, TravisCI and Heroku;
- TDD.

## Tech stack
The project uses the following technologies:
- Back end: Python, using Django
- AI (object detection, text extraction): MS Azure services
- Storage (for images provided, files generated): Azure blob storage
- Front end: HTML / CSS / JavaScript. Main JS library used is d3.js
- Hosting and logs: Heroku
