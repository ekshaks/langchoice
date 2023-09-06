import sys

sys.path.insert(0, '..')


'''
at any state 
match user_msg
-> if trigger msg -> trigger conv-flow. goto state or stay.
-> elif state-dep msg -> state-dep conv-flow, goto state_
-> else -> state.sorry_repeat

'''

def run_conversation():
    assistant_state = 0
    while True:
        say__(assistant_state)
        user_response = get_response__()
        response_id = match__(user_response, template_graph[assistant_state])
        assistant_state = update_state(assistant_state, response_id)

        if is_terminal__(assistant_state, template_graph):
            break;
'''
def run_conversation2():
    state = 'start'
    while True:
        say__(bot_msgs.at_state[state])
        if is_terminal__(state): break
        user_msg = input('User: ')
        actions, next_state = get_next__(user_msg, state)
        execute_actions()
        state = next_state
'''

def update_state(state, next_state):
    print(f'Updating state from {state} to {next_state}')
    #TODO: assistant action
    return next_state.split('.', 1)[1]

def load_data(filename='appo.yaml'):
    import yaml
    with open(filename, "r") as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            raise exc
    
    print(data) #(cat | sent*)
    return data['flow'], data['assistant_msgs'], data['user_msgs']

def run_c(conv_data, start='interested_q'):
    flows, assistant_msgs, user_msgs = conv_data
    appo_flow = flows['appointment']
    from langchoice import LangStore
    state = start
    
    #print(user_msgs)
    S = LangStore(user_msgs, name='appointment1', rebuild=True)
    while True:
        assistant_msg = assistant_msgs[state]
        print(f'Assistant: {assistant_msg}')

        user_msg = input('User: ')
        msg_actions = appo_flow[state]
        mtype, _ = S.match(user_msg, debug=True, debug_k=5)
        mtype = f'user.{mtype}'
        if mtype in msg_actions:
            state = update_state(state, msg_actions[mtype])
        else:
            raise ValueError(f'Invalid message: {mtype}')


if __name__ == '__main__':
    D = load_data()
    run_c(D)