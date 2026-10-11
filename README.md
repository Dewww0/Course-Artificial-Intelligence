## Overview

This project implements a complete Rule-Based Expert System for Medical Diagnosis using Forward and Backward Chaining algorithms, with a modern web interface built using Streamlit. The system demonstrates classical AI reasoning techniques from Russell & Norvig's "Artificial Intelligence: A Modern Approach" without using any machine learning.

## Features Implemented

### Core AI Algorithms
- **Forward Chaining (Data-Driven):** Starts with symptoms and derives all possible diagnoses
- **Backward Chaining (Goal-Driven):** Tests if a specific diagnosis can be proven from given symptoms
- **Working Memory Management:** Tracks facts and reasoning chains during inference
- **Explanation Facility:** Provides step-by-step reasoning transparency with visual graphs

### Knowledge Base
- 15 medical IF-THEN rules covering common conditions
- Confidence levels and explanations for each rule
- Covers diagnoses: Common Cold, Influenza, Strep Throat, Migraine, Allergic Reactions, etc.
- Treatment recommendations linked to diagnoses

### User Interface
- Modern web interface using Streamlit
- Symptom input via checkboxes
- Real-time diagnosis with both inference methods
- Visual and textual explanation of reasoning

## System Architecture

```
┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│   Web Interface      │    │ Inference Engine     │    │ Knowledge Base       │
│  (Streamlit)         │◄──►│   - Forward Chaining │◄──►│   - Rules            │
│                      │    │   - Backward Chaining│    │   - Facts            │
└──────────────────────┘    └──────────────────────┘    └──────────────────────┘
         │                          │                        
         │                 ┌──────────────────────┐         
         │                 │ Working Memory       │         
         │                 │ - Facts              │         
         │                 │ - Reasoning Chain    │         
         └─────────────────┤                      │         
                           └──────────────────────┘         
                                    │                      
                           ┌──────────────────────┐         
                           │  Explanation Module  │         
                           └──────────────────────┘         
```

## Main Files

- `app.py` - Streamlit web app entry point
- `expert_system_core.py` - Core expert system logic and inference engine
- `medical_knowledge_base.py` - Medical rules and facts database
- `requirements.txt` - Python dependencies
- `README (1).md` - Project documentation (this file)

## How to Run

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the web app:
   ```bash
   streamlit run app.py
   ```
3. Open your browser to the URL shown in the terminal (usually http://localhost:8501)

## Example Usage

### Forward Chaining
1. Select symptoms using the checkboxes in the "Symptom Input" tab.
2. Click "Submit Symptoms".
3. Go to the "Forward Chaining" tab and click "Run Forward Chaining".
4. Diagnoses and recommendations will be displayed, along with the inference process.

### Backward Chaining
1. After submitting symptoms, go to the "Backward Chaining" tab.
2. Select a diagnosis or recommendation to verify.
3. Click "Verify Goal" to see if it can be proven from the current facts.

### Explanation Facility
1. After running inference, go to the "Explanation" tab.
2. Select a derived fact to see a step-by-step and visual explanation of how it was inferred.

## Technical Highlights

### Forward Chaining Algorithm
- Data-driven inference with iterative rule application
- Monotonic reasoning with fact accumulation
- Conflict resolution through rule ordering
- Guaranteed termination with finite rule sets

### Backward Chaining Algorithm
- Goal-driven inference with recursive proof search
- Depth-first search with cycle detection
- Confidence propagation through proof chains
- Efficient pruning of impossible goals

### Explanation System
- Step-by-step reasoning traces
- Rule application tracking
- Confidence level propagation
- Human-readable and visual explanations for all inferences

## Educational Value

This project demonstrates:
- **Classical AI Reasoning:** Rule-based expert systems
- **Search Algorithms:** Forward and backward chaining
- **Knowledge Representation:** IF-THEN rules with confidence
- **Inference Mechanisms:** Logical reasoning without ML
- **Explanation Systems:** Transparent AI decision-making

## Disclaimer

This system is for educational purposes only and should not be used for actual medical diagnosis. Always consult qualified healthcare professionals for medical advice.
