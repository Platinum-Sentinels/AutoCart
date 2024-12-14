import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Dense, Concatenate, Flatten, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from tensorflow.keras.callbacks import ReduceLROnPlateau

# Step 1: Define the TensorFlow Model
def build_model():
    # Input Layers
    query_input = Input(shape=(100,), name="query_input")  # Tokenized query
    platform_input = Input(shape=(1,), name="platform_input")  # Encoded platform
    price_input = Input(shape=(1,), name="price_input")  # Product price
    rating_input = Input(shape=(1,), name="rating_input")  # Product rating

    # Embedding layers for text data
    embedding_query = Embedding(input_dim=10000, output_dim=64)(query_input)
    embedding_query = Flatten()(embedding_query)

    # Concatenate all features
    merged = Concatenate()([embedding_query, platform_input, price_input, rating_input])

    # Dense layers for prediction
    x = Dense(256, activation='relu')(merged)  # Increased number of units
    x = Dropout(0.3)(x)  # Increased dropout to prevent overfitting
    x = Dense(128, activation='relu')(x)
    output = Dense(1, activation='sigmoid', name="relevance_score")(x)

    # Create the model
    model = Model(inputs=[query_input, platform_input, price_input, rating_input], outputs=output)

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    return model

# Step 2: Preprocess Data
def preprocess_data(queries, platforms, prices, ratings):
    tokenizer = Tokenizer(num_words=10000)
    tokenizer.fit_on_texts(queries)

    # Tokenize and pad queries
    tokenized_queries = tokenizer.texts_to_sequences(queries)
    tokenized_queries = pad_sequences(tokenized_queries, maxlen=100)

    # Normalize numeric data
    prices = np.array(prices).reshape(-1, 1)
    ratings = np.array(ratings).reshape(-1, 1)

    # Encode platforms (e.g., Amazon -> 0, eBay -> 1)
    platform_mapping = {"Amazon": 0, "eBay": 1}
    encoded_platforms = np.array([platform_mapping[platform] for platform in platforms]).reshape(-1, 1)

    return tokenized_queries, encoded_platforms, prices, ratings

# Step 3: Augmented Training Data (e.g., Random Sampling)
def augment_data(queries, platforms, prices, ratings, relevance_scores):
    # You can randomly shuffle data or apply small perturbations
    indices = np.random.permutation(len(queries))
    queries = np.array(queries)[indices]
    platforms = np.array(platforms)[indices]
    prices = np.array(prices)[indices]
    ratings = np.array(ratings)[indices]
    relevance_scores = np.array(relevance_scores)[indices]
    return queries, platforms, prices, ratings, relevance_scores

# Step 4: Train the Model and Print Results
def train_and_print_results():
    # Example training data
    queries = ["msi katana gf66", "gaming laptop", "budget laptop", "high-performance laptop", "cheap laptop"]  # Example queries
    platforms = ["Amazon", "eBay", "Amazon", "Amazon", "eBay"]
    prices = [1200, 900, 1500, 800, 600]
    ratings = [4.5, 4.2, 4.8, 4.3, 4.0]
    relevance_scores = [0.9, 0.7, 0.95, 0.8, 0.65]  # Simulated relevance scores

    # Preprocess data
    tokenized_queries, encoded_platforms, prices, ratings = preprocess_data(queries, platforms, prices, ratings)

    # Augment data (random shuffle)
    tokenized_queries, encoded_platforms, prices, ratings, relevance_scores = augment_data(
        tokenized_queries, encoded_platforms, prices, ratings, relevance_scores)

    # Build and train the model
    model = build_model()

    # Reduce learning rate when validation loss plateaus
    lr_scheduler = ReduceLROnPlateau(monitor='loss', factor=0.5, patience=3, min_lr=1e-6)

    model.fit(
        [tokenized_queries, encoded_platforms, prices, ratings],
        np.array(relevance_scores),
        epochs=20,
        batch_size=32,
        validation_split=0.2,
        callbacks=[lr_scheduler]
    )

    # Save the model
    model.save("product_recommendation_model.h5")
    print("Model training complete and saved as 'product_recommendation_model.h5'.")

    # Step 5: Predict relevance scores and display results
    predicted_scores = model.predict([tokenized_queries, encoded_platforms, prices, ratings])

    # Print the results
    print("\nPredicted Relevance Scores:")
    for i in range(len(queries)):
        print({
            "Query": queries[i],
            "Platform": platforms[i],
            "Price": prices[i],
            "Rating": ratings[i],
            "Actual Relevance Score": relevance_scores[i],
            "Predicted Relevance Score": predicted_scores[i][0]
        })

# Main Execution
if __name__ == "__main__":
    try:
        # Train the model and display the results
        train_and_print_results()

    except ImportError as e:
        print("TensorFlow or necessary dependencies are not installed. Please install them to proceed.")
    except Exception as ex:
        print(f"An error occurred: {ex}")
