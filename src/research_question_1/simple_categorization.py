import os
import json


def read_json_file(file_path):
    print(f"Reading file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def categorize_conversation(prompt, answer):
    prompt = prompt.lower()
    answer = answer.lower()

    if "bug" in prompt or "error" in answer:
        category = "Bug"
    elif "feature" in prompt or "implement" in answer:
        category = "Feature Request"
    elif "how to" in prompt or "why" in answer:
        category = "Theoretical Question"
    else:
        category = "Other"

    return category


def process_json_files(directory):
    categories_count = {
        "Bug": 0,
        "Feature Request": 0,
        "Theoretical Question": 0,
        "Other": 0,
    }

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
                            category = categorize_conversation(prompt, answer)
                            categories_count[category] += 1

    return categories_count


def main():
    directory = "../../snapshots"
    print("Starting analysis...")
    result = process_json_files(directory)

    print("\nTotal conversations:", sum(result.values()))
    print("Analysis complete. Results:")
    for category, count in result.items():
        print(f"\t{category}: {count}")


if __name__ == "__main__":
    main()
