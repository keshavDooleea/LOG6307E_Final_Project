import os
import json


def read_json_file(file_path):
    print(f"Reading file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def process_json_files(directory):
    structure = {
        "NumberOfPrompts": [],
        "TokensOfPrompts": [],
        "TokensOfAnswers": [],
        "ListOfCode": 0,
        "TotalConversations": 0,
    }

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                data = read_json_file(file_path)

                for source in data.get("Sources", []):
                    chatgpt_sharing = source.get("ChatgptSharing", [])
                    for sharing in chatgpt_sharing:
                        number_of_prompts = sharing.get("NumberOfPrompts")
                        if number_of_prompts is not None or "":
                            structure["NumberOfPrompts"].append(number_of_prompts)

                        number_of_tokens_per_prompts = sharing.get("TokensOfPrompts")
                        if number_of_tokens_per_prompts is not None or "":
                            structure["TokensOfPrompts"].append(
                                number_of_tokens_per_prompts
                            )

                        number_of_tokens_per_answers = sharing.get("TokensOfAnswers")
                        if number_of_tokens_per_answers is not None or "":
                            structure["TokensOfAnswers"].append(
                                number_of_tokens_per_answers
                            )

                        # Get number of conversations having code
                        for conversation in sharing.get("Conversations", []):
                            structure["TotalConversations"] += 1
                            list_of_code = conversation.get("ListOfCode", [])
                            if len(list_of_code) > 0:
                                structure["ListOfCode"] += 1

    return structure


def find_average(data):
    return sum(data) / len(data)


def main():
    directory = "../../snapshots"
    print("Starting analysis...")
    result = process_json_files(directory)

    print("\nAnalysis complete. Results:")

    print("\tNumber of total conversations: ", result["TotalConversations"])
    print("\tNumber of conversations having code: ", result["ListOfCode"])

    print(
        "\tAverage number of prompts in a conversations: ",
        find_average(result["NumberOfPrompts"]),
    )
    print(
        "\tAverage number of words in a question of a conversation: ",
        find_average(result["TokensOfPrompts"]),
    )
    print(
        "\tAverage number of words in an answer of a conversation: ",
        find_average(result["TokensOfAnswers"]),
    )


if __name__ == "__main__":
    main()
