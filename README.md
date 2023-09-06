

![License](https://img.shields.io/github/license/ekshaks/langchoice)
![PyPi](https://img.shields.io/pypi/v/langchoice)

PyPI: <a href="https://pypi.org/project/langchoice/" target="_blank">https://pypi.org/project/langchoice</a></br>


## 🤖 About LangChoice

`switch-case`, but for free-form sentences. A one-liner for `if-then-else` over similar sentences.

The LangChoice library allows you to condition your structured programs over natural language sentence predicates or triggers. Makes it easy to define conditional flows over user inputs without implementing the sentence *match* operator over and over again.


## 📦 Installation
```
pip install langchoice
```

## 🧪 Getting Started

Suppose we want to detect if an incoming user message *triggered* belongs to one of the following (*greeting*, *politics*) topics. Do this in a few lines using `langchoice`.

First define the text messages that define each topic category (a message group).

```python
triggers =\
'''
greeting:
    - hello
    - hi
    - what's up?

politics:
    - what are your political beliefs?
    - thoughts on the president?
    - left wing
    - right wing
'''
```

1. Set up a `LangStore` data container.

```python
data = yaml.safe_load(triggers)
S = LangStore(data)
```

2. On receiving a user message `user_msg`, simply match with topics!

```python
match S.match(user_msg, threshold=1.2, debug=True): 
    case 'greeting', _ : #user_msg matches the greeting message cluster
        say_hello()
    case 'politics', _ : #user_msg matches the politics message cluster
        change_topic()
    case x :
        print(x)
        print(f'No defined triggers detected. Ask an LLM for response.')
```

Add or remove sentences from each topic or introduce new topics. Works on-the-fly!

Supports multiple matching modes:

* `S.match` returns the topic of nearest message.
* Use `S.match_centroid` to instead find the nearest topic *centroid* .
* (Optional) Provide thresholds for the *no-topic-matches* case:
    - `S.match` returns `None` if the nearest topic distance is greater than the threshold.


## Debug and More!

* Use `debug=True` and `debug_k=5` to 
    - display distance of `user_msg` to different topics.
    - Get match scores for each message group to debug what went wrong.


Coming Soon!
- In built assertions, which fail if the execution fails to match the expected topic / group.
* Compute the thresholds automatically for pre-specified message groups against a query evaluation set
* Fine-tune embeddings to *separate* message clusters better.


### Implement a Conversation Flow with Message-based Routing

The langchoice package enables you to make controlled chatbot flows as well as build guardrails very quickly.

The key motivation is to allow users to have maximal control when designing the bot:
- add/update messages on demand
- route user messages to owner states or modules
- more control over conversation flow, without losing ability to chitchat
- build conversations, not (worry about) LLM chains!

For example, see a sales lead filtering and appointment-booking bot under [examples](examples/).

- Specify the assistant and user messages as well as the overall conversation flow in a yaml file easily
- Automate the conversational flow with few lines of code
- Add messages and modify the flow effortlessly by modifying the yaml
    - Model picks up the changes instantly, no need to fine-tune models for the changes


## Roadmap

- [ ] match variants
    - [ ] hybrid match - match regex separately
    - [ ] local S.match (based on state tag)
    - [ ] match type='item' (default) | type='group' (centroid) | ...
- [ ] allow switching under-the-hood sentence encoders
- [ ] fine-tune based on in-topic and irrelevant messages



## Author

Nishant Sinha, Founder, Consulting Scientist, OffNote Labs. 

For insights on Generative AI evolution and applications, follow on [Linkedin](https://www.linkedin.com/in/nishant-sinha-a610311/), and read our articles on [Substack](https://offnote.substack.com/).

