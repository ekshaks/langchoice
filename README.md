

![License](https://img.shields.io/github/license/ekshaks/langchoice)
![PyPi](https://img.shields.io/pypi/v/langchoice)

PyPI: <a href="https://pypi.org/project/langchoice/" target="_blank">https://pypi.org/project/langchoice</a></br>


## 🤖 About LangChoice

`switch-case`, but for free-form sentences. A one-liner for `if-then-else`` over similar sentences.

The LangChoice library allows you to condition your structured programs over natural language sentence predicates or triggers. Makes it easy to define conditional flows over user inputs without implementing the sentence *match* operator over and over again.


## 📦 Installation
```
pip install langchoice
```

## 🧪 Getting Started

Suppose you want to detect if the user mentioned one of the following (*greeting*, *politics*) triggers:

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

2. On receiving a user message `user_msg`, simply match!

```python
match S.match(user_msg): 
    case 'greeting', _ : #user_msg matches any of the greeting message cluster
        say_hello()
    case 'politics', _ : #user_msg matches any of the politics message cluster
        change_topic()
    case x :
        print(x)
        print(f'No defined triggers detected. Ask an LLM for response.')
```


## Do More!

### Implement a graph-based Conversation Flow



## Debug

- Get match scores for each group to debug what went wrong.


- In built assertions, which fail if the execution fails to match the expected topic / group.


## Roadmap

- [] allow switching under-the-hood sentence encoders

