# Langchoice demo examples

## Sales Filtering and Scheduling Bot

- Specify the `assistant` and `user` template messages as well as the overall conversation `flow` in a yaml file easily
- Define multiple flows as `user-message: goto next-state` format.
- Automate the conversational flow with few lines of [code](conv-template-bot.py)
- Add messages and modify the flow effortlessly by modifying the yaml
    - Model picks up the changes instantly, no need to fine-tune models for the changes