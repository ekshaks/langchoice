
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

from lang_conditions import LangStore


def load_rules():
    import yaml
    data = yaml.safe_load(triggers)
    print(data) #(cat | sent*)
    S = LangStore(data)
    return S

def execute_conv_flow__(category):
    '''
    Lookup topic -> [msg]. send msgs
    '''
    print(f'executing conv_flow for {category}')

def test_two_topics(S: LangStore, user_msg):
    match S.lang_check(user_msg): 
        case topic, _ if topic in ['politics', 'greeting']:
            execute_conv_flow__(topic)
        case x :
            print(x)
            print(f'no triggers. ask llm.')



if __name__ == '__main__':
    S = load_rules()
    test_two_topics(S, 'hello friend of the government')
    test_two_topics(S, 'define politics of the world')
    #index_or_query()



