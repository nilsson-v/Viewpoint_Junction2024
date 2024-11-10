# Viewpoint

**Enhancing Citizen Discourse through News, AI, and Real-Time Engagement**

---

## Project Overview

Viewpoint is a platform that aims to elevate public discourse by merging credible news with vibrant, real-time conversations. It empowers users to explore reliable news articles, voice their opinions, and join meaningful discussions, creating an inclusive space where every perspective matters. By transforming how we consume news and engage with diverse viewpoints, Viewpoint seeks to foster a more informed and engaged digital democracy.

## Features

1. **Reliable News Integration**: Access trustworthy news sources to stay informed on politics, social issues, and global events.

2. **Dynamic Conversations**: Engage in real-time discussions with other users, ensuring that every voice can be heard.

3. **Opinion Clustering with pol.is**: Visualize public opinion through pol.is, a tool that allows users to upvote or downvote comments, observe opinion clusters, and find common ground or identify extremes.

4. **AI-Driven Functionality**:
   - **Advanced Search**: Use AI to deliver smart, context-aware search results, helping users find relevant discussions and news effortlessly.
   - **Intelligent Chat Integration**: Benefit from AI-supported chat that can facilitate discussions, answer questions, and provide insights.
   - **Opinion Clustering and Analytics**: Viewpoint’s AI clusters opinions intelligently to reveal patterns in public sentiment, promoting a clearer understanding of different perspectives.

5. **Extensibility with pol.is API**: With an API key, users can unlock enhanced data analytics and integration capabilities in pol.is, providing deeper insights and improved interactivity.

## Technology Stack

- **Backend**: Flask, containerized and deployed to Google Cloud Run for a scalable and reliable backend infrastructure.
- **Frontend**: React, deployed on Vercel for a performant, responsive user interface.
- **AI and LLM Integration**: Uses GROQ for large language model (LLM) capabilities to power intelligent features like search, chat, and opinion processing.
- **Opinion Visualization**: Pol.is integration for clustering opinions and visualizing public sentiment.

## Installation and Setup

### Prerequisites

- Docker
- Node.js and npm
- Python 3.9
- A Google Cloud account (for deployment on Cloud Run)
- Vercel account (for frontend deployment)

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/nilsson-v/junction2024.git
   cd viewpoint
   ```

2. **Backend Setup**:

   - Navigate to the backend directory.
   - Create a virtual environment and activate it:

     ```bash
     python3 -m venv env
     source env/bin/activate
     ```

   - Install the required dependencies:

     ```bash
     pip install -r requirements.txt
     ```

   - Configure environment variables for Flask and Google Cloud.

   - Build and run the Docker image:

     ```bash
     docker build -t firebase_backend .
     docker run -p 8000:8000 firebase_backend
     ```

3. **Frontend Setup**:

   - Navigate to the frontend directory.
   - Install dependencies:

     ```bash
     npm install
     ```

   - Start the development server:

     ```bash
     npm run dev
     ```

4. **Deployment**:

   - Deploy the backend to Google Cloud Run following the Google Cloud deployment guide.
   - Deploy the frontend to Vercel via the Vercel CLI or GitHub integration.

## Usage

1. **Explore News**: Browse through curated, reliable news sources directly on the platform.
2. **Join Conversations**: Share your opinions on news topics and engage with other users in real-time discussions.
3. **Pol.is Integration**: Visualize public sentiment, understand opinion clusters, and explore areas of consensus or difference.
4. **Advanced Search and Chat**: Utilize AI-driven search and chat for personalized news discovery and enhanced interactions.

## Check it out here:

https://junction2024-ear6hpyx1-daniel-michaelis-projects.vercel.app/
