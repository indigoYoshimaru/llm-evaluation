# LLM Evaluator

The CLI to create test set and evaluate your model and RAG pipeline. 
For dataset generation, we support Question-Answering dataset type while

## Installation
1. Clone the project, change dir to the project folder and run: 
   ```
   pip install . 
   ```
2. To view the help menu, run: 
   ```
   llm-eval [command] --help 
   ```
   
3. To init the CLI, run `llm-eval init [path-to-your-env-file]`. Eg: 
   ```
   llm-eval init llm-evaluation/.vscode/launch.json
   ```
4. You can modify the files in `llm_evaluator/configs` to meet your settings
5. 
##  Dataset Synthesis

## Evaluation

### Model/General pipeline

### RAG

## Other docs

## TODO: 
- [ ] Create multiple datasets at once
- [ ] Evaluate on multiple datasets at once
- [ ] Update metrics info
- [ ] Add UI for configs settings
- [ ] Add dataset viewer and modification platform
- [ ] Evaluation results registry