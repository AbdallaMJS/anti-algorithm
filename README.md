# The Anti-Algorithm: Explainable Recommendation Logic

An innovative, explainable recommendation prototype designed to challenge user preferences by suggesting choices outside their usual comfort zone. Unlike traditional machine learning models that often act as opaque "black boxes," this system is fully transparent. It maps user preferences across six interpretable dimensions, calculates normalized Euclidean distance to find the most contrasting options, and explicitly explains the largest differences behind each result.

## 🌟 Key Features

- **Explainable AI (XAI) Principles:** Fully transparent recommendation logic where every suggestion is accompanied by a breakdown of why it was chosen based on specific dimensional clashes.
- **Distance-Based Recommendation:** Uses normalized Euclidean distance to identify items that are furthest from a user's typical preferences, purposefully avoiding similarity.
- **Interactive Taste Profiling:** Users input their standard preferences across various categories, generating a real-time 6-dimensional taste profile.
- **Visual Clashes:** Displays visual comparison bars highlighting the largest gaps between the user's profile and the recommended opposite item.
- **Taste Shift Tracking:** Allows users to record their reactions to unusual recommendations over time, measuring "Taste Flexibility" and tracking whether unfamiliar choices lead to curiosity, rejection, or new preferences.
- **Clean, Modern Interface:** Built with Streamlit, featuring a redesigned interface with sidebar controls, large result cards, and a cohesive visual identity.

## 🛠️ Technologies Used

- **Language:** Python
- **Framework:** Streamlit
- **Data Handling:** Pandas, NumPy
- **Mathematics:** Euclidean Geometry (Normalized Distance Calculations)

## 💡 How It Works

1. **Profile Generation:** Users select their usual preferences within a specific category. Each selection contributes weighted values to six distinct, interpretable dimensions (e.g., in movies, dimensions might be 'Action', 'Intellectual', 'Pacing', etc.).
2. **Distance Calculation:** The system compares the aggregated user profile vector against a curated dataset of potential recommendations. It calculates the normalized Euclidean distance for every item.
3. **Contrasting Recommendation:** The algorithm ranks the dataset by distance, prioritizing the items that are furthest from the user's profile (the "Anti-Match").
4. **Transparent Explanation:** The top recommendation is presented not just as a choice, but with a detailed breakdown. The system identifies and visually displays the specific dimensions with the largest numerical gaps between the user and the item.
5. **Reaction Recording:** Users can optionally save their reaction to the recommendation, feeding data into the "Taste Shift" tracker to monitor evolving preferences.

## 🚀 Setup and Installation

To run this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AbdallaMJS/anti-algorithm.git
   cd anti-algorithm
   ```

2. **Set up a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

## 🧠 Educational Value & MBZUAI Relevance

This project demonstrates a foundational understanding of core artificial intelligence concepts, specifically focusing on **Explainable AI (XAI)** and distance-based algorithms. Rather than relying on imported, pre-trained black-box models, it implements the underlying mathematical logic (Euclidean distance) from scratch to ensure complete transparency. This aligns closely with the rigorous analytical and mathematical approach expected in advanced AI undergraduate programs like the one at MBZUAI. It showcases practical problem-solving, algorithm design, and user-centric data presentation.

## 🔮 Future Enhancements

- **Dynamic Datasets:** Integrating external APIs (like TMDB or Spotify) to calculate distances on a live, vast dataset rather than a curated list.
- **Weight Adjustments:** Allowing users to manually tweak the importance of different dimensions in their profile.
- **Machine Learning Integration:** Slowly introducing ML models to predict *which* contrasting dimensions a user is most likely to eventually appreciate, moving from pure distance calculation to predictive contrast.

---
*Developed by Abdalla M.J.S. Alblooshi as part of a technical portfolio demonstrating early competency in explainable AI logic and Python software engineering.*
