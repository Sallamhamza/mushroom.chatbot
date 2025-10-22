Mushroom Expert Chatbot
A multimodal AI chatbot powered by Gemini/HuggingFace that specializes in mushroom identification and information. The chatbot can analyze mushroom images and provide expert knowledge about various mushroom species.
Overview
This project implements an intelligent chatbot capable of:

Answering questions about mushrooms
Processing and analyzing mushroom images
Providing structured identification data in JSON format
Maintaining context-aware conversations about mycology

Features

Multimodal Capabilities: Processes both text queries and mushroom images
Expert System Prompting: Behaves as a mushroom expert with guided conversations
Streaming Responses: Real-time text generation with chunk-by-chunk display
Structured Output: JSON-formatted identification data for parsed images
Safety Filters: (Gemini) Built-in content safety mechanisms
Error Handling: Graceful failure recovery with conversation rewind support

Implementation Tasks
Core Functionality

Gemini/HuggingFace Integration

Add chatbot to the interface
Configure API connections


Multimodal Support

Enable image processing capabilities
Support mushroom photo analysis


System Prompting

Implement mushroom expert persona
Guide conversations toward mushroom-related topics


Streaming Implementation

Display text chunks in real-time
Handle progressive response rendering


Safety Filter Handling (Gemini only)

Display messages when safety filters trigger
Implement appropriate user notifications


Error Recovery (Gemini only)

Add try-catch blocks for streaming failures
Implement conversation rewind functionality


Structured Image Analysis

Generate JSON responses for mushroom images with fields:

common_name: Common name of the mushroom
genus: Scientific genus
confidence: Prediction confidence (0-1)
visible: Array of visible parts (["cap", "hymenium", "stipe"])
color: Mushroom color in the image
edible: Boolean edibility status



Example Output:

json   {
     "common_name": "Inkcap",
     "genus": "Coprinus",
     "confidence": 0.5,
     "visible": ["cap", "hymenium", "stipe"],
     "color": "orange",
     "edible": true
   }

Log JSON to console (not displayed in chat)
Maintain context for follow-up questions


Contextual Response Logic

If user asks a question with image: Answer the question after processing
If no question provided: Generate summary from JSON data



Evaluation Questions
1. Classification Accuracy
Assess the model's mushroom classification capabilities. Consider:

Quality of predictions across different species
Handling of incomplete information (e.g., parasol mushroom with missing stipe)
Edge cases and failure modes

2. Prediction Consistency

Test reproducibility by classifying the same image multiple times
Implement temperature=0.0 for deterministic outputs
Identify other potential causes of inconsistent predictions

3. Prompt Engineering Security

Attempt to make the chatbot discuss non-mushroom topics
Evaluate difficulty of breaking out of the mushroom domain
Propose improvements to make it more robust

4. Text Recognition

Test OCR capabilities with nya_svampboken_p226.jpg
Evaluate transcription quality
Identify missing or reinterpreted content

5. Safety Considerations

Gemini: Assess risks of lowering safety filters for text transcription
HuggingFace: Evaluate risks of missing safety filters and mitigation strategies

6. JSON Output Validation

Verify correct JSON format generation
Check accuracy of field values
Validate summary-JSON correspondence

7. Answer Quality Assessment

Test with mushroom_*.jpg images from data folder
Compare performance across model complexities
Document limitations of the expert system

8. Ethical Information Handling

Test Amanita Muscaria (fly agaric) information provision
Ensure proper warnings about neurotoxin risks
Implement safeguards against dangerous misuse

9. User Engagement

Propose methods to improve chatbot engagement
Implement conversational improvements

Deliverables
Submit via Canvas:

Report following the Overleaf template
Source code implementation
Example chatbot responses for each exercise
Analysis and answers to evaluation questions

Notes

Temperature setting affects reproducibility but doesn't guarantee consistency
Some exercises have multiple valid solutions
Evaluation focuses on implementation quality, conceptual understanding, and creative assessment
