#!/bin/bash

# Navigate to the research_question_1 directory
cd research_question_1

# Ask the user to choose an option
echo 
echo "Select an option:"
echo "1. Run simple categorization"
echo "2. Run model categorization"
read -p "Enter your choice (1 or 2): " choice
echo

# Run the appropriate Python script based on the user's choice
if [ "$choice" = "1" ]; then
    echo "Running simple_categorization.py"
    python simple_categorization.py
elif [ "$choice" = "2" ]; then
    echo "Running model_categorization.py"
    python model_categorization.py
else
    echo "Invalid choice. Please run the script again and select either 1 or 2."
fi
