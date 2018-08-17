import numpy as np 

class TreeNode:
    '''
    Monte Carlo Tree
    '''
    def __init__(self,parent,prior_p):
        self._parent = parent
        self._childern = {} # Save childre nodes in Hash data structure
        self._n_visits = 0
        self._Q = 0
        self._u = 0
        self._P = prior_p

    def expand(self,action_priors):
        '''
        Expand Leaf Node
        '''
        for action, prob in action_priors:
            if action not in self._childern:
                self._childern[action] = TreeNode(self,prob)

    def select(self,c_puct):
        '''
        Select node based on PUCT algorithm
        '''
        return max(self._childern.items(),
            key=lambda action_node: action_node[1].get_value(c_puct)
            )

    def update(self,leaf_value):
        '''
        Update node based on value
        '''
        self._n_visits += 1
        self._Q += 1.0*(leaf_value - self._Q) / self._n_visits

    def update_recursive(self, leaf_value):
        '''
        Update node and its parents' node based on value
        '''
        if self._parent:
            self._parent.update_recursive(leaf_value)
        self.update(leaf_value)

    def get_value(self,c_puct):
        '''
        Get PUCT value of node
        '''
        self._u = (c_puct * self._P * np.sqrt(self._parent._n_visits) / (1 + self._n_visits))
        return self._Q + self._u

    def is_leaf(self):
        return self._childern == {}



class MCTS:
    def __init__(self,model,size,L=10):
        '''
        Monte Carlo Tree Search: Self play algorithm
        '''
        self.states = list()
        self.actions = list()
        self.N = list()
        self.W = list()
        self.Q = list()
        self.P = list()
        self.model = model
        self.L = L

    def expand(self,state):
        '''
        Return values in Monte Carlo Tree:
            N(s,a), W(s,a), Q(s,a), P(s,a)

        Actions:
            a = 1: Left
            a = 2: Right
            a = 3: Up
            a = 4: Down
        '''
        actions = [1,2,3,4]
        if  len(self.states) == 0:
            self.states.append(state)
            self.N.append(0)
            self.W.append(0)
            self.Q.append(0)

            Ps,a = self.model.execute(state)
            
            self.P.append(Ps)
            self.actions.append(action)

        for i in range(self.states):


    def update(self,state,action):


class MCTS:
    '''
    Monte Carlo Tree Search: Improver of deep learning model
    '''
    def __init__(self, evaluate_function, c_puct, n_playout, verbose=False):
        self.root = TreeNode(None, 1.0)
        self.evaluate_function = evaluate_function
        self.c_puct = c_puct
        self.n_playout = n_playout
        self.verbose = verbose

    def search(self, engine, temperature):
        '''
        Search best action based on MCTS simulations
        '''
        for i in range(self.n_playout):
            _engine = engine.clone()
            if self.root.is_leaf():
                # Expand and Evaluate
                state = engine.get_state()
                probs, value = self.evaluate_function(state)

                actions = np.arange(5)
                self.root.expand(zip(actions, probs))

                # Backup
                self.root.update(value)
            else:
                # Select 
                action, node = self.root.select(self.c_puct)
                _engine.play(action)
                while not node.is_leaf():
                    action, node = node.select(self.c_puct)
                    _engine.play(action)

                # Expand and Evaluate
                state = _engine.get_state()
                probs, value = self.evaluate_function(state)

                actions = np.arange(5)
                node.expand(zip(actions, probs))

                # Backup
                node.update_recursive(value)

        # Play: Return simulation results
        actions_visits = [(action, node._n_visits) for action, node in self.root._childern.items()]
        actions, visits = zip(*actions_visits)
        action_probs = softmax(1.0/temperature*np.log(np.array(visits) + eps))
        return actions, action_probs

    def play(self, engine, s_mcts=True):
        '''
        Play game according to the information from game engine
        '''
        n_simulations = 10  # Number of MCTS simulations
        c_puct = 0.95   
        n_playout = 10  # Depth of Monte Carlo Tree (Number of playout)

        if s_mcts:
            # Run MCTS simulations
            n_actions = np.zeros(5)
            for i in range(self.n_simulations):
                _engine = engine.clone()
                mcts = MCTS(
                    evaluate_function=self.evaluate_function, 
                    c_puct=c_puct, 
                    n_playout=n_playout, 
                    verbose=self.verbose)
                )
                mcts_actions, probs = mcts.search(engine=_engine)
                action = np.random.choice(
                    mcts_actions,
                    p=0.75*probs + 0.25*np.random.dirichlet(0.3*np.ones(len(probs)))
                )
                n_actions[action] += 1
            action = np.argmax(n_actions)
        else:
            # Evaluate state directly
            state = engine.get_state()
            probs, value = self.evaluate_function(state=state)
            actions = np.arange(5)
            action = np.random.choice(
                actions,
                p=0.75*probs + 0.25*np.random.dirichlet(0.3*np.ones(len(probs)))
                )

        return action