# Prompt-Pandemic-restinPython
FactScope: AI News Verifier
FactScope is a modern, responsive web application designed to help users verify the authenticity of news articles, images, and headlines. Using a clean and intuitive interface, it simulates an AI-powered verification process to categorize news content and combat misinformation.

✨ Features
Multi-Format Input: Users can submit a news URL, upload a news-related image, or type in a headline for verification.

Categorized Results: The verification results are clearly categorized into "Fully True," "Partially True," and "Fully False" sections.

Interactive Follow-Up:

For "Partially True" news, users can request a summary to understand the context.

For "Fully False" news, users can request to see the potential reason for its spread.

Stylish & Modern UI: A sleek, dark-themed design with custom fonts and smooth transitions provides a professional user experience.

Responsive Design: The layout is fully responsive and works seamlessly on desktops, tablets, and mobile devices.

🛠️ Technologies Used
Frontend: HTML5, CSS3

Fonts:

'Logo': Custom font using NewYork PERSONAL USE.otf by Artem Nevsky.

'Fonk': Custom font using Bitcount Prop Single Ink (a.ttf).

Space Grotesk: Imported from Google Fonts for headings.

Libre Franklin: Imported from Google Fonts.

📂 Project Structure
.
├── index.html          # The main HTML file for the application structure.
├── style.css           # The CSS file for all styling and layout.
├── a.ttf               # Font file for 'Fonk' (Bitcount Prop Single Ink).
├── NewYork PERSONAL USE.otf # Font file for 'Logo'.
└── png.png             # Background pattern image.
🚀 Getting Started
This is a frontend-only project. No special installation is required.

Clone the repository:

Bash

git clone <your-repository-link>
Navigate to the project directory:

Bash

cd <repository-name>
Open the application:
Simply open the index.html file in your favorite web browser.

📝 How It Works
The user lands on the homepage and is presented with a form.

They can choose to input a news URL, upload an image, or enter a headline.

Upon clicking "Verify News," the results section becomes visible.

The application simulates an AI analysis and places the result in the appropriate category (Fully True, Partially True, or Fully False).

If the news is partially true or false, a "Next Steps" section appears, offering buttons to get more details like a summary or the reason for misinformation.

Clicking these buttons reveals the detailed information in an output box.

Note: The current implementation is a frontend prototype. The verification logic in index.html is a placeholder to demonstrate the UI flow. A full implementation would require a backend service with an AI/ML model to process the inputs and return actual verification results.

⚖️ Credits & License
NewYork Font: Copyright (c) 2020 by Artem Nevsky. Free for personal use.

Bitcount Prop Single Ink Font: Copyright 2024 The Bitcount Project Authors, licensed under the SIL Open Font License.

Background Image: The png.png file provides the background pattern.
