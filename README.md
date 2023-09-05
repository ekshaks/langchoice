

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

Suppose you want to detect if the user message *triggered* one of the following (*greeting*, *politics*) categories.

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

Supports multiple matching modes:

* `S.match` returns the topic of nearest message.
* Use `S.match_centroid` to instead find the nearest topic *centroid* .
* (Optional) Provide thresholds for the *no-topic-matches* case:
    - `S.match` returns `None` if the nearest topic distance is greater than the threshold.

## Debug and More!

* Use `debug=True` and `debug_k=5` to 
    - visualize distance of `user_msg` to topics.
    - Get match scores for each message group to debug what went wrong.


Coming Soon!
- In built assertions, which fail if the execution fails to match the expected topic / group.
* Compute the thresholds automatically for pre-specified message groups against a query evaluation set
* Fine-tune embeddings to *separate* message clusters better.


### Implement a graph-based Conversation Flow


## Roadmap

- [ ] allow switching under-the-hood sentence encoders

