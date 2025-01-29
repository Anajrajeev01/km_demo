from flask import Flask, jsonify, render_template_string, request
import logging

app = Flask(__name__)

# Configure Logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Company Data
company_info = {
    "name": "Unisys Pvt Ltd",
    "industry": "IT Services & Consulting",
    "headquarters": "Blue Bell, Pennsylvania, USA",
    "founded": 1986,
    "services": ["Cloud Computing", "Cybersecurity", "AI Solutions", "Data Analytics"],
    "website": "https://www.unisys.com/"
}

# HTML & CSS UI in Python String
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unisys Pvt Ltd - Company Info</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #90EE90; margin: 20px; padding: 20px; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        h1 { color: #0073e6; text-align: center; }
        p { font-size: 16px; line-height: 1.6; }
        .card { padding: 10px; background: #f9f9f9; border-radius: 5px; margin-bottom: 10px; }
        ul { list-style-type: none; padding: 0; }
        ul li { background: #0073e6; color: white; padding: 8px; margin: 5px 0; border-radius: 5px; text-align: center; }
        a { text-decoration: none; color: #0073e6; font-weight: bold; }
        input, button { padding: 10px; width: 100%; margin-top: 10px; }
        button { background: #0073e6; color: white; border: none; cursor: pointer; }
        button:hover { background: #005bb5; }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ company.name }}</h1>
        <p><strong>Industry:</strong> {{ company.industry }}</p>
        <p><strong>Headquarters:</strong> {{ company.headquarters }}</p>
        <p><strong>Founded:</strong> {{ company.founded }}</p>
        <p><strong>Website:</strong> <a href="{{ company.website }}" target="_blank">{{ company.website }}</a></p>
        
        <h3>Services Offered:</h3>
        <ul>
            {% for service in company.services %}
                <li>{{ service }}</li>
            {% endfor %}
        </ul>

        <div class="card">
            <h3>Search for a Service</h3>
            <input type="text" id="serviceInput" placeholder="Enter service name...">
            <button onclick="searchService()">Search</button>
            <p id="result"></p>
        </div>
    </div>

    <script>
        function searchService() {
            let serviceName = document.getElementById("serviceInput").value;
            fetch(`/api/search?service=${serviceName}`)
                .then(response => response.json())
                .then(data => {
                    let resultText = document.getElementById("result");
                    if (data.status === "success") {
                        resultText.innerHTML = "✅ Service Found: " + data.matching_services.join(", ");
                        resultText.style.color = "green";
                    } else {
                        resultText.innerHTML = "❌ Service Not Found";
                        resultText.style.color = "red";
                    }
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    """
    Renders the Home Page with Company Details
    """
    logging.info("Home page accessed.")
    return render_template_string(HTML_TEMPLATE, company=company_info)

@app.route('/api/company', methods=['GET'])
def get_company_info():
    """
    API Endpoint: Returns company information in JSON format
    """
    logging.info("Company API accessed.")
    return jsonify(company_info)

@app.route('/api/search', methods=['GET'])
def search_service():
    """
    API Endpoint: Search a service offered by Unisys Pvt Ltd
    """
    query = request.args.get('service', '').lower()
    matching_services = [service for service in company_info['services'] if query in service.lower()]

    if matching_services:
        logging.info(f"Service '{query}' found.")
        return jsonify({"status": "success", "matching_services": matching_services})
    
    logging.warning(f"Service '{query}' not found.")
    return jsonify({"status": "error", "message": "Service not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
