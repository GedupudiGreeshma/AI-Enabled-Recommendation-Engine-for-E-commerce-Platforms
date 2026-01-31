## Milestone 1: Data Preparation ✅

### Objective

Prepare clean and structured datasets for recommendation model development.

### Tasks Completed

* Collected and explored the e-commerce dataset
* Removed duplicates and handled missing values
* Cleaned user and product interaction data
* Constructed the user–item interaction matrix

### Files

* `data/processed/cleaned_data.csv` – cleaned dataset
* `data/processed/user_item_matrix.csv` – user–item interaction matrix
* `notebooks/data_preparation.ipynb` – data preprocessing notebook

### Status

✔️ Milestone 1 completed successfully

---

## Milestone 2: Recommendation Model Building ✅

### Objective

Develop and train a recommendation model using the prepared e-commerce dataset.

### Model Selection

A **User–Category Collaborative Filtering** approach was implemented.

* Users are represented by their category-level interactions
* Categories act as items in the user–item matrix (Product IDs were replaced with categories to address sparsity)
* Cosine similarity is used to compute user similarity
* This approach enables similarity computation despite single-product interactions

### Model Architecture

* User–Item Matrix (User × Category)
* Implicit interaction modeling
* Matrix normalization using L2 normalization
* Cosine similarity for user similarity computation
* Top-N recommendation logic
* Popularity-based fallback mechanism for cold-start users

### Training Process

* Constructed a user–category interaction matrix
* Normalized the interaction matrix
* Computed user similarity using cosine similarity
* Generated recommendations based on preferences of similar users

### Evaluation Metrics (Initial Analysis)

* Matrix sparsity
* Recommendation coverage
* Average user similarity

These metrics provide an initial understanding of model behavior under data constraints.

### Key Observations

* Due to single interaction per user, similarity signals are weak
* Recommendations frequently fall back to globally popular categories
* This behavior is expected in cold-start and sparse data scenarios

### Limitations

* No repeated user interactions
* No explicit rating data
* Limited personalization capability

### Status

✅ Recommendation model successfully developed and trained
✅ Initial evaluation completed
✅ Milestone 2 objectives met

---

## Milestone 3: Evaluation and Refinement ✅

### Objective

Evaluate the performance of the recommendation model and refine it to improve accuracy and reliability.

### Evaluation Methodology

The model developed in Milestone 2 was evaluated using standard recommendation system metrics:

* Precision
* Recall
* F1-score

Evaluation was performed using a **Top-K recommendation strategy**, where K values of 3, 5, and 10 were tested to analyze performance under different recommendation list sizes.

### Metrics Used

* **Precision@K**: Measures the relevance of recommended categories
* **Recall@K**: Measures the model’s ability to retrieve relevant categories
* **F1-score@K**: Provides a balanced evaluation of precision and recall

### Model Refinement

* Tested multiple values of K (Top-3, Top-5, Top-10)
* Observed trade-offs between precision and recall
* Identified optimal K based on balanced F1-score

### Key Results

* The model achieved consistently high precision, indicating highly relevant recommendations
* Recall improved as the value of K increased
* The F1-score showed significant improvement for higher K values, demonstrating effective refinement

### Scenario Testing

* Users with minimal interaction history
* Users with relatively higher interaction signals

The model showed stable behavior across scenarios, with popularity-based recommendations effectively handling sparse and cold-start cases.

### Observations

* High precision indicates conservative but accurate recommendations
* Lower recall is expected due to sparse interaction data
* Increasing K improves coverage and recall without degrading precision

### Status

✅ Model performance validated using precision, recall, and F1-score
✅ Model refined through Top-K tuning
✅ Milestone 3 objectives met