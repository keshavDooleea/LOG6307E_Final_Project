import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load and prepare the machine learning model
print("Training model...")
df = pd.read_csv("training_set.csv")
X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42
)
vectorizer = TfidfVectorizer(max_features=1000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)
print("Training model complete.\n")


def read_json_file(file_path):
    print(f"Reading file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def combined_categorization(prompt, answer, model, vectorizer):
    combined_text = prompt + " " + answer
    transformed_text = vectorizer.transform([combined_text])
    return model.predict(transformed_text)[0]


def process_json_files(directory, model, vectorizer):
    categories_count = {
        "Bug": 0,
        "Feature Request": 0,
        "Theoretical Question": 0,
        "Other": 0,
    }
    results = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                data = read_json_file(file_path)

                for source in data.get("Sources", []):
                    chatgpt_sharing = source.get("ChatgptSharing", [])
                    for sharing in chatgpt_sharing:
                        for conversation in sharing.get("Conversations", []):
                            prompt = conversation.get("Prompt", "")
                            answer = conversation.get("Answer", "")
                            category = combined_categorization(
                                prompt, answer, model, vectorizer
                            )
                            categories_count[category] += 1

                            # Only add to results if category is not 'Other'
                            if category != "Other":
                                results.append(
                                    {
                                        "prompt": prompt,
                                        "answer": answer,
                                        "category": category,
                                    }
                                )

    return categories_count, results


def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Results written to {filename}")


def main():
    directory = "../../snapshots/"
    print("Starting analysis...")
    categories_count, categorized_data = process_json_files(
        directory, model, vectorizer
    )

    print("\nTotal conversations:", len(categorized_data))
    print("Analysis complete. Results:")
    for category, count in categories_count.items():
        print(f"\t{category}: {count}")

    # Split data into separate lists based on category
    bugs = [item for item in categorized_data if item["category"] == "Bug"]
    feature_requests = [
        item for item in categorized_data if item["category"] == "Feature Request"
    ]
    theoretical_questions = [
        item for item in categorized_data if item["category"] == "Theoretical Question"
    ]

    # Save each category to its own CSV file
    print("\n")
    save_to_csv(bugs, "bugs.csv")
    save_to_csv(feature_requests, "feature_requests.csv")
    save_to_csv(theoretical_questions, "theoretical_questions.csv")


if __name__ == "__main__":
    main()
