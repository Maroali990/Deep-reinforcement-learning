import numpy as np
class sarsa2():
    
    
    NUM_STATES = 19 # number of states (not including the ending state)
    START = 9
    END_0 = 0
    END_1 = 20

    def __init__(self, n, start=START, end=False, lr=0.1, gamma=1, debug=False):
            self.actions = ["left", "right"]
            self.state = start  # current state
            self.end = end
            self.n = n
            self.lr = lr
            self.gamma = gamma
            self.debug = debug
            # init q estimates
            self.Q_values = {}
            for i in range(self.NUM_STATES + 2):
                self.Q_values[i] = {}
                for a in self.actions:
                    if i in [self.END_0, self.END_1]:
                        # explicitly set end state values
                        if i == self.END_0:
                            self.Q_values[i][a] = -1
                        else:
                            self.Q_values[i][a] = 1
                    else:
                        self.Q_values[i][a] = 0

    def chooseAction(self):
            action = np.random.choice(self.actions)
            return action

    def takeAction(self, action):
            new_state = self.state
            if not self.end:
                if action == "left":
                    new_state = self.state - 1
                else:
                    new_state = self.state + 1

                if new_state in [self.END_0, self.END_1]:
                    self.end = True
            self.state = new_state
            return self.state

    def play(self, rounds=100):
            for _ in range(rounds):
                self.reset()
                t = 0
                T = np.inf
                action = self.chooseAction()

                actions = [action]
                states = [self.state]
                rewards = [0]
                while True:
                    if t < T:
                        state = self.takeAction(action)  # next state
                        reward = self.giveReward()  # next state-reward

                        states.append(state)
                        rewards.append(reward)

                        if self.end:
                            if self.debug:
                                print("End at state {} | number of states {}".format(state, len(states)))
                            T = t + 1
                        else:
                            action = self.chooseAction()
                            actions.append(action)  # next action
                    # state tau being updated
                    tau = t - self.n + 1
                    if tau >= 0:
                        G = 0
                        for i in range(tau + 1, min(tau + self.n + 1, T + 1)):
                            G += np.power(self.gamma, i - tau - 1) * rewards[i]
                        if tau + self.n < T:
                            state_action = (states[tau + self.n], actions[tau + self.n])
                            G += np.power(self.gamma, self.n) * self.Q_values[state_action[0]][state_action[1]]
                        # update Q values
                        state_action = (states[tau], actions[tau])
                        self.Q_values[state_action[0]][state_action[1]] += self.lr * (
                                    G - self.Q_values[state_action[0]][state_action[1]])

                    if tau == T - 1:
                        break

                    t += 1