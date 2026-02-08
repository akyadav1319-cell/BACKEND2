"""
National Policy Command Centre (NPCC) - Backend API
Flask server with routes for policy simulation and AI news generation
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Import core engine
from backend.core.engine import PolicyEngine

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for local development

# Initialize Policy Engine
policy_engine = PolicyEngine()

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBE1ok5qIXh9mOLl2fgVLXzAeKAJlhmWBU")
genai.configure(api_key=GEMINI_API_KEY)


@app.route('/api/init', methods=['GET'])
def initialize_dashboard():
    """
    GET /api/init
    Returns the 2026 baseline state for dashboard initialization

    Response:
        {
            "year": 2026,
            "temperature_anomaly": 1.2,
            "temperature_formatted": "+1.20°C",
            "national_debt": 0,
            "national_debt_formatted": "$0.00B",
            "policies": {...},
            "bau_projection": [...],
            "historical_data": [...]
        }
    """
    try:
        baseline_state = policy_engine.get_baseline_state()
        return jsonify({
            "success": True,
            "data": baseline_state
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/calculate', methods=['POST'])
def calculate_policy_impact():
    """
    POST /api/calculate
    Calculate fiscal cost and temperature mitigation based on policy inputs

    Request Body:
        {
            "ev_adoption": 0-100,
            "renewable_energy": 0-100,
            "carbon_tax": 0-100,
            "reforestation": 0-100
        }

    Response:
        {
            "success": true,
            "data": {
                "total_cost": 245.6,
                "total_cost_formatted": "$245.60B",
                "temperature_mitigation": -0.28,
                "temperature_mitigation_formatted": "-0.280°C",
                "national_debt": 245.6,
                "national_debt_formatted": "$245.60B",
                "bankruptcy_flag": false,
                "policy_breakdown": [...],
                "trend_line": [...],
                "fiscal_treemap": [...],
                "efficiency_index": [...],
                "warning_message": null
            }
        }
    """
    try:
        # Get JSON payload
        policy_inputs = request.get_json()

        if not policy_inputs:
            return jsonify({
                "success": False,
                "error": "Missing policy inputs"
            }), 400

        # Calculate impacts using policy engine
        results = policy_engine.calculate_impacts(policy_inputs)

        return jsonify({
            "success": True,
            "data": results
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/news', methods=['POST'])
def generate_news_headline():
    """
    POST /api/news
    Generate AI-powered news headline based on current policy configuration
    Uses Gemini Pro model to create realistic 2035 press secretary headline

    Request Body:
        {
            "ev_adoption": 0-100,
            "renewable_energy": 0-100,
            "carbon_tax": 0-100,
            "reforestation": 0-100,
            "temperature_change": -0.28,  // Optional context
            "fiscal_cost": 245.6  // Optional context
        }

    Response:
        {
            "success": true,
            "data": {
                "headline": "Prime Minister Announces Landmark Climate Victory: National Emissions Drop 28% Ahead of 2035 Target",
                "policy_summary": {...}
            }
        }
    """
    try:
        # Get JSON payload
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Missing input data"
            }), 400

        # Extract policy levels
        ev_level = data.get("ev_adoption", 0)
        renewable_level = data.get("renewable_energy", 0)
        carbon_tax_level = data.get("carbon_tax", 0)
        reforestation_level = data.get("reforestation", 0)

        # Optional context
        temp_change = data.get("temperature_change", 0)
        fiscal_cost = data.get("fiscal_cost", 0)

        # Construct prompt for Gemini
        prompt = f"""You are a senior government press secretary in the year 2035. 
Write a professional, confident 1-sentence headline announcing the results of the national climate policy program.

Current Policy Implementation Levels (0-100 scale):
- EV Adoption Incentives: {ev_level}%
- Renewable Energy Expansion: {renewable_level}%
- Carbon Tax Implementation: {carbon_tax_level}%
- Reforestation Programs: {reforestation_level}%

Additional Context:
- Temperature mitigation achieved: {temp_change}°C
- Total fiscal investment: ${fiscal_cost}B

Write ONE headline that sounds like it came from a government press conference. Be specific, use numbers when relevant, and convey a sense of achievement or urgency depending on the policy levels.

Examples of good headlines:
- "Prime Minister Announces Historic Climate Victory as National Emissions Drop 32% Below 2020 Levels"
- "Government Commits $180B to Renewable Energy Revolution, Targeting 75% Clean Grid by 2040"
- "Treasury Reports $50B Revenue Gain from Carbon Tax as Industries Pivot to Green Technologies"

Your headline:"""

        # Call Gemini API
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        headline = response.text.strip()

        # Remove quotes if present
        if headline.startswith('"') and headline.endswith('"'):
            headline = headline[1:-1]
        if headline.startswith("'") and headline.endswith("'"):
            headline = headline[1:-1]

        return jsonify({
            "success": True,
            "data": {
                "headline": headline,
                "policy_summary": {
                    "ev_adoption": ev_level,
                    "renewable_energy": renewable_level,
                    "carbon_tax": carbon_tax_level,
                    "reforestation": reforestation_level,
                    "temperature_impact": temp_change,
                    "fiscal_cost": fiscal_cost
                }
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"AI generation failed: {str(e)}"
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """
    GET /health
    Simple health check endpoint
    """
    return jsonify({
        "status": "healthy",
        "service": "NPCC Backend API",
        "version": "1.0.0"
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


if __name__ == '__main__':
    # Run Flask development server
    # Production: Use gunicorn or uwsgi
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True

    )

