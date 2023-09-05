
# example from https://www.pinecone.io/learn/nemo-guardrails-intro/

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

flows = \
'''
politics:
    - sorry
greeting:
    - hello
'''



from .langchoice import LangStore


def load_db(index=False):
    import yaml
    data = yaml.safe_load(triggers)
    print(data) #(cat | sent*)
    S = LangStore(data)
    if index:
        S.index()
    return S

def execute_conv_flow__(category):
    '''
    Lookup intent -> [msg]. send msgs
    '''
    print(f'executing conv_flow for {category}')

def match_then_exec(S: LangStore, user_msg, debug=False):
    match S.match(user_msg, threshold=1.2, debug=debug, debug_k=5): 
        case topic, _ if topic in ['politics', 'greeting']:
            execute_conv_flow__(topic)
        case x :
            print(f'No predefined triggers. Ask LLM!')


import pytest

@pytest.fixture
def inputs():
    S = load_db(index=False)
   
    qs = [
        'hello citizens of the nation',
        'define politics of the region',
        'meet tomorrow at 10?'

    ]
    return S, qs

def test_nearest(inputs):
    # test match (nearest element)
    S, qs = inputs
    for q in qs:
        match_then_exec(S, q, debug=True)

def test_centroid(inputs):
    # test match_centroid
    S, qs = inputs

    for q in qs:
        S.match_centroid(q, debug=True)

if __name__ == '__main__':
    #S.index(reset=True)
    test_nearest(inputs())



