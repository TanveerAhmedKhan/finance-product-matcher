# Product Name Matcher - Documentation

## Overview

The Product Name Matcher is a powerful NLP-based tool designed to help finance teams standardize inconsistent product names across sales and inventory files. It uses advanced natural language processing techniques to identify similar product names, group them together, and generate standardized names for reporting and analysis.

## Key Features

1. **Token-based Matching**: Breaks down product names into meaningful tokens and matches them based on shared tokens.
2. **TF-IDF Similarity**: Uses Term Frequency-Inverse Document Frequency to calculate vector-based similarity between product names.
3. **Hybrid Matching**: Combines token-based and TF-IDF approaches for more accurate matching.
4. **Variant Protection**: Prevents grouping products with conflicting variants (e.g., "iPhone 13 Pro" vs "iPhone 13 Mini").
5. **Size Protection**: Prevents grouping products with different sizes (e.g., "32in TV" vs "50in TV").
6. **Confidence Scoring**: Assigns confidence scores to each match to indicate reliability.
7. **Manual Review Flagging**: Flags low-confidence matches for manual review.
8. **Fully Local Processing**: All processing happens locally, with no external API calls or data transmission.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. Clone or download this repository to your local machine.
2. Open a terminal or command prompt and navigate to the repository directory.
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

### Using the Launcher Scripts

#### Windows
Double-click the `run_matcher.bat` file to launch the application.

#### macOS/Linux
1. Make the launcher script executable:
   ```bash
   chmod +x run_matcher.sh
   ```
2. Run the script:
   ```bash
   ./run_matcher.sh
   ```

### Manual Launch

Alternatively, you can run the application manually:

```bash
streamlit run product_matcher_final.py
```

## Docker Deployment

### Prerequisites for Docker

- Docker installed on your system
- Basic knowledge of Docker commands

### Building and Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t product-name-matcher .
   ```

2. Run the container:
   ```bash
   docker run -p 8080:8080 product-name-matcher
   ```

3. Access the application in your web browser at:
   ```
   http://localhost:8080
   ```

### Docker Configuration

The Dockerfile is configured to:
- Use Python 3.9 as the base image
- Install all required dependencies
- Download necessary NLTK data
- Expose port 8080
- Configure Streamlit to listen on all interfaces (0.0.0.0) and port 8080

## Google Cloud Run Deployment

### Prerequisites for Cloud Run

- Google Cloud account
- Google Cloud SDK installed and configured
- Docker installed
- Appropriate permissions on your Google Cloud project

### Deployment Steps

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

### Cloud Run Configuration

The deployment script configures the Cloud Run service with:
- 1GB of memory
- Public access (--allow-unauthenticated)
- The us-central1 region (configurable in the script)

### Customizing the Deployment

You can modify the deployment scripts to:
- Change the region
- Adjust memory allocation
- Add environment variables
- Configure authentication requirements
- Set up custom domains

## Using the Application

### 1. Upload Files

- **Sales File**: Upload a CSV file containing product sales data. The file must have at least two columns:
  - `Product`: The product name
  - `Sales (£)`: The sales amount in pounds

- **Inventory File**: Upload a CSV file containing product inventory data. The file must have at least two columns:
  - `Product`: The product name
  - `Inventory Units`: The inventory quantity

### 2. Configure Matching Settings

- **Matching Method**:
  - **Token-based**: Uses exact token matching (best for structured names)
  - **TF-IDF Similarity**: Uses vector similarity (best for unstructured names)
  - **Hybrid**: Combines both approaches (recommended for most cases)

- **Minimum Similarity Score**: The threshold for considering products as matches (0.0-1.0)
  - Higher values (e.g., 0.8) result in stricter matching
  - Lower values (e.g., 0.5) result in more lenient matching

- **Variant Protection**: When enabled, prevents grouping products with conflicting variants

- **Size Protection**: When enabled, prevents grouping products with different sizes

- **Manual Review Threshold**: Confidence score below which products are flagged for manual review

### 3. View Results

The application provides two main views:

#### Matched Results

Shows the standardized product names with aggregated data:
- **Standardized Name**: The cleaned, standardized product name
- **Sales (£)**: Total sales for all products mapped to this standardized name
- **Inventory Units**: Total inventory units for all products mapped to this standardized name

#### Matching Summary

Shows the mapping details:
- **Product**: The original product name
- **Standardized Name**: The standardized name it was mapped to
- **Confidence**: The confidence score of the match (as a percentage)
- **Flag**: Any flags for the match (e.g., "Manual Review Needed")

You can filter the summary view:
- Show only items flagged for review
- Filter by minimum confidence score

### 4. Download Results

Both the matched results and matching summary can be downloaded as CSV files for further analysis or reporting.

## How It Works

### 1. Tokenization

The application breaks down product names into meaningful tokens. For example:
- "Samsung TV 32in Smart" → ['samsung', 'tv', '32', 'smart']
- "32in Samsung Smart TV" → ['32', 'samsung', 'smart', 'tv']

### 2. Feature Extraction

The application extracts key features from product names:
- **Brand**: Identifies potential brand names (e.g., "Samsung", "Apple")
- **Size**: Extracts size information (e.g., "32in", "500ml")
- **Variants**: Identifies variant information (e.g., "Pro", "Mini", "Smart")

### 3. Similarity Calculation

Depending on the selected method, the application calculates similarity between products:
- **Token-based**: Uses Jaccard similarity (intersection over union of tokens)
- **TF-IDF**: Uses cosine similarity between TF-IDF vectors
- **Hybrid**: Combines both approaches with weighted averaging

### 4. Grouping

Products with similarity above the threshold are grouped together, respecting variant and size protection settings.

### 5. Standardization

For each group, the application generates a standardized name based on:
- The most common brand
- The most common product type tokens
- The most common size
- Specific variant information

### 6. Confidence Scoring

Each match is assigned a confidence score based on:
- Similarity between the original and standardized name
- Presence of variant or size conflicts
- Token overlap quality

### 7. Aggregation

Sales and inventory data are aggregated by standardized product names to create the final output.

## Best Practices

1. **Start with Default Settings**: Begin with the default settings and adjust as needed.
2. **Review Flagged Items**: Always review items flagged for manual review.
3. **Iterative Refinement**: Adjust settings and re-run if needed to improve results.
4. **Consistent Naming**: For best results, try to maintain some consistency in your original product naming.
5. **Pre-processing**: Consider cleaning your data before uploading (e.g., fixing obvious typos).

## Troubleshooting

### Common Issues

1. **File Format Errors**:
   - Ensure your CSV files have the correct column names
   - Check for special characters or encoding issues in your files

2. **No Matches Found**:
   - Try lowering the minimum similarity threshold
   - Check if variant or size protection is preventing matches

3. **Incorrect Grouping**:
   - Increase the minimum similarity threshold
   - Enable variant and size protection if disabled

4. **Performance Issues**:
   - For large files, consider splitting them into smaller batches
   - Close other resource-intensive applications

## Advanced Usage

### Custom Preprocessing

If you need to customize the preprocessing logic, you can modify the `preprocess_text` function in the source code.

### Adding New Features

To add support for new product features or attributes, you can extend the feature extraction functions in the source code.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
