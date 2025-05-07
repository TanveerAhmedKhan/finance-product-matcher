# Product Name Matcher

A backend automation tool for finance teams that cleans and merges messy product names across sales and inventory files using NLP-based matching.

## Features

- **Token-based matching logic** to group similar product names (e.g., "Samsung TV 32", "32in Samsung Smart TV")
- **Variant conflict protection** to prevent grouping different variants (e.g., "iPhone 13" vs "iPhone 13 Pro")
- **Fully local operation** - no API calls or external services (for confidential finance data)
- **No glossary/dictionary required** - matching relies on smart rule-based NLP logic
- **Output summary** showing original values, standardized names, confidence scores, and flags

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit application using one of the following methods:

**Windows:**
```
run_matcher.bat
```

**macOS/Linux:**
```bash
chmod +x run_matcher.sh
./run_matcher.sh
```

Or run directly with Streamlit:
```bash
streamlit run product_matcher_final.py
```

This will open the application in your default web browser.

### Using the Application

1. **Upload Files**:
   - Upload your sales CSV file (must contain 'Product' and 'Sales (£)' columns)
   - Upload your inventory CSV file (must contain 'Product' and 'Inventory Units' columns)

2. **Adjust Settings** (optional):
   - Minimum Similarity Score: Threshold for considering products similar
   - Variant Protection: Enable/disable variant conflict detection
   - Size Protection: Enable/disable size conflict detection
   - Manual Review Threshold: Confidence score below which products are flagged

3. **View Results**:
   - Matched Results: Shows standardized product names with aggregated sales and inventory data
   - Matching Summary: Shows original product names, their standardized versions, confidence scores, and flags

4. **Download Results**:
   - Download the matched results and summary tables as CSV files

## File Format

The application expects CSV files with the following structure:

### Sales File
```
Product,Sales (£)
Samsung TV 32in S,459
Sam TV 32in,876
Samsung TV,831
Samsung TV Smart,990
```

### Inventory File
```
Product,Inventory Units
Samsung TV 32in S,91
Sam TV 32in,21
Samsung TV,42
Samsung TV Smart,42
```

## Docker Deployment

You can run this application in a Docker container:

1. Build the Docker image:
```bash
docker build -t product-name-matcher .
```

2. Run the container:
```bash
docker run -p 8080:8080 product-name-matcher
```

3. Access the application at http://localhost:8080

## Google Cloud Run Deployment

To deploy this application to Google Cloud Run:

1. Update the `PROJECT_ID` in the deployment script:
   - For Linux/macOS: Edit `deploy-to-cloud-run.sh`
   - For Windows: Edit `deploy-to-cloud-run.bat`

2. Run the deployment script:
   - For Linux/macOS:
     ```bash
     chmod +x deploy-to-cloud-run.sh
     ./deploy-to-cloud-run.sh
     ```
   - For Windows:
     ```
     deploy-to-cloud-run.bat
     ```

3. The script will:
   - Build the Docker image
   - Push it to Google Container Registry
   - Deploy it to Cloud Run
   - Output the URL where your application is available

### Prerequisites for Cloud Run Deployment

- Google Cloud SDK installed and configured
- Docker installed
- Authenticated with Google Cloud (`gcloud auth login`)
- Appropriate permissions on your Google Cloud project

## How It Works

1. **Tokenization**: Product names are broken down into meaningful tokens
2. **Similarity Calculation**: Token-based similarity is calculated between products
3. **Conflict Detection**: Variant and size conflicts are detected to prevent incorrect grouping
4. **Standardization**: Similar products are grouped and given standardized names
5. **Confidence Scoring**: Each match is given a confidence score
6. **Aggregation**: Sales and inventory data are aggregated by standardized product names

## License

This project is licensed under the MIT License - see the LICENSE file for details.
