#!/bin/bash

# Function to run RQ1 script
run_rq1() {

    echo "Running RQ1 script..."

    # Navigate to the research_question_1 directory
    cd research_question_1

    # Ask the user to choose an option for RQ1
    echo
    echo "Select an option for RQ1:"
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

    # Return to the original directory
    cd ..
}

# Function to run RQ2 script
run_rq2() {
    echo
    echo "Running RQ2 script..."

    # Navigate to the research_question_2 directory
    cd research_question_2

    python main.py
}

# Function to choose between RQ1 and RQ2
main() {
    # Ask the user to choose an option between RQ1 and RQ2
    echo
    echo "Select a Research Question (RQ) to run:"
    echo "1. Run RQ1"
    echo "2. Run RQ2"
    read -p "Enter your choice (1 or 2): " choice
    echo

    # Run the appropriate Python script based on the user's choice
    if [ "$choice" = "1" ]; then
        run_rq1
    elif [ "$choice" = "2" ]; then
        run_rq2
    else
        echo "Invalid choice. Please run the script again and select either 1 or 2."
    fi
}

# Execute RQs
main