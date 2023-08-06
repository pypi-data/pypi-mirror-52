from abc import ABCMeta, abstractmethod
import torch
import torch.nn as nn
import numpy as np
from collections import deque
import random
from .memories import BasicMemory


class BaseAgent(metaclass=ABCMeta):

    @abstractmethod
    def act(self, states):
        pass

    @abstractmethod
    def step(self, state, action, reward, next_state, done):
        pass

    @staticmethod
    def soft_update(local_model, target_model, tau):
        """Soft update model parameters.
        θ_target = τ*θ_local + (1 - τ)*θ_target
        Params
        ======
            local_model: PyTorch model (weights will be copied from)
            target_model: PyTorch model (weights will be copied to)
            tau (float): interpolation parameter
        """
        for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
            target_param.data.copy_(tau*local_param.data + (1.0-tau)*target_param.data)

    @abstractmethod
    def save(self, filename):
        pass

    def epoch_finished(self):
        pass

    def run(self, env, epochs, score_threshold, filename):
        all_scores = []
        scores_window = deque(maxlen=100)

        for epoch in range(1, epochs+1):

            state = env.reset()
            score = 0

            while True:
                action = self.act(state)
                next_state, reward, done, _ = env.step(action)
                self.step(state, action, reward, next_state, done)

                score += reward
                state = next_state

                if done:
                    break

            self.epoch_finished()
            avg_score = np.mean(score)
            scores_window.append(avg_score)
            all_scores.append(avg_score)

            print('\rEpisode {}\tAverage Score: {:.2f}'.format(epoch, np.mean(scores_window)), end="")
            if epoch % 100 == 0:
                print('\rEpisode {}\tAverage Score: {:.2f}'.format(epoch, np.mean(scores_window)))
            if np.mean(scores_window) >= score_threshold:
                print('\nEnvironment solved in {:d} episodes!\tAverage Score: {:.2f}'.format(epoch, np.mean(scores_window)))
                self.save(filename=filename)
                break

        return all_scores


class DQNAgent(BaseAgent):
    def __init__(self,
                 device,
                 actor,
                 actor_optimizer,
                 memory_size,
                 batch_size,
                 update_every,
                 discount,
                 soft_update_tau,
                 eps_start,
                 eps_end,
                 eps_decay,
                 ):
        self.device = device
        self.update_every = update_every
        self.discount = discount
        self.soft_update_tau = soft_update_tau
        self.t_step = 0
        self.eps = eps_start
        self.eps_end = eps_end
        self.eps_decay = eps_decay
        self.action_size = list(actor.parameters())[-1].shape[0]

        # Actor Network (w/ Target Network)
        self.actor_local = actor
        self.actor_target = type(actor)()
        self.actor_optimizer = actor_optimizer
        self.actor_target.eval()

        # Memory
        self.memory = BasicMemory(memory_size=memory_size, batch_size=batch_size, device=device)

        # ----------------------- initialize target networks ----------------------- #
        self.soft_update(self.actor_local, self.actor_target, 1)

    def act(self, states):
        """Returns actions for given state as per current policy."""
        states = torch.from_numpy(states).float().to(self.device)
        self.actor_local.eval()
        with torch.no_grad():
            actions = self.actor_local(states).cpu().data.numpy()
        self.actor_local.train()

        # Epsilon-greedy action selection
        if random.random() > self.eps:
            return np.argmax(actions)
        else:
            return random.randint(0, self.action_size - 1)

    def step(self, state, action, reward, next_state, done):
        # Save experience in replay memory
        self.memory.add(state, action, reward, next_state, done)

        # Learn every UPDATE_EVERY time steps.
        self.t_step = (self.t_step + 1) % self.update_every
        if self.t_step == 0:
            # If enough samples are available in memory, get random subset and learn
            if len(self.memory) > self.memory.batch_size:
                experiences = self.memory.sample()
                self.learn(experiences, self.discount)

    def learn(self, experiences, gamma):
        """Update value parameters using given batch of experience tuples.
        Params
        ======
            experiences (Tuple[torch.Variable]): tuple of (s, a, r, s', done) tuples
            gamma (float): discount factor
        """

        states, actions, rewards, next_states, dones = experiences

        # Get max predicted Q values (for next states) from target model
        Q_targets_next = self.actor_target(next_states).detach().max(1)[0].unsqueeze(1)
        # Compute Q targets for current states
        Q_targets = rewards + (gamma * Q_targets_next * (1 - dones))

        # Get expected Q values from local model
        Q_expected = self.actor_local(states).gather(1, actions.long())

        # Compute loss
        loss = nn.MSELoss()
        actor_local_loss = loss(Q_expected, Q_targets)
        # Minimize the loss
        self.actor_optimizer.zero_grad()
        actor_local_loss.backward()
        self.actor_optimizer.step()

        # ------------------- update target network ------------------- #
        self.soft_update(self.actor_local, self.actor_target, self.soft_update_tau)

    def save(self, filename):
        torch.save(self.actor_local.state_dict(), 'actor_' + filename)

    def epoch_finished(self):
        self.eps = max(self.eps_end, self.eps_decay * self.eps)


class DDPGAgent(BaseAgent):
    def __init__(self,
                 device,
                 actor,
                 actor_optimizer,
                 critic,
                 critic_optimizer,
                 memory_size,
                 batch_size,
                 update_every,
                 discount,
                 soft_update_tau,
                 ):

        self.device = device
        self.update_every = update_every
        self.discount = discount
        self.soft_update_tau = soft_update_tau
        self.t_step = 0

        # Actor Network (w/ Target Network)
        self.actor_local = actor
        self.actor_target = type(actor)()
        self.actor_optimizer = actor_optimizer

        # Critic Network (w/ Target Network)
        self.critic_local = critic
        self.critic_target = type(critic)()
        self.critic_optimizer = critic_optimizer

        # Memory
        self.memory = BasicMemory(memory_size=memory_size, batch_size=batch_size, device=device)

        # ----------------------- initialize target networks ----------------------- #
        self.soft_update(self.actor_local, self.actor_target, 1)
        self.soft_update(self.critic_local, self.critic_target, 1)

    def act(self, states):
        """Returns actions for given state as per current policy."""
        states = torch.from_numpy(states).float().to(self.device)
        self.actor_local.eval()
        with torch.no_grad():
            actions = self.actor_local(states).cpu().data.numpy()
        self.actor_local.train()
        return np.clip(actions, -1, 1)

    def step(self, state, action, reward, next_state, done):
        # Save experience in replay memory
        self.memory.add(state, action, reward, next_state, done)

        # Learn every UPDATE_EVERY time steps.
        self.t_step = (self.t_step + 1) % self.update_every
        if self.t_step == 0:
            # If enough samples are available in memory, get random subset and learn
            if len(self.memory) > self.memory.batch_size:
                experiences = self.memory.sample()
                self.learn(experiences, self.discount)

    def learn(self, experiences, gamma):
        """Update policy and value parameters using given batch of experience tuples.
        Q_targets = r + γ * critic_target(next_state, actor_target(next_state))
        where:
            actor_target(state) -> action
            critic_target(state, action) -> Q-value
        Params
        ======
            experiences (Tuple[torch.Tensor]): tuple of (s, a, r, s', done) tuples
            gamma (float): discount factor
        """

        states, actions, rewards, next_states, dones = experiences

        # ---------------------------- update critic ---------------------------- #
        # Get predicted next-state actions and Q values from target models
        actions_next = self.actor_target(next_states).float()
        Q_targets_next = self.critic_target(next_states, actions_next)
        # Compute Q targets for current states (y_i)
        Q_targets = rewards + (gamma * Q_targets_next * (1 - dones))
        # Compute critic loss
        Q_expected = self.critic_local(states, actions)
        loss = nn.MSELoss()
        critic_loss = loss(Q_expected, Q_targets)
        # Minimize the loss
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        torch.nn.utils.clip_grad_norm_(self.critic_local.parameters(), 1)
        self.critic_optimizer.step()

        # ---------------------------- update actor ---------------------------- #
        # Compute actor loss
        actions_pred = self.actor_local(states).float()
        actor_loss = -self.critic_local(states, actions_pred).mean()
        # Minimize the loss
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()

        # ----------------------- update target networks ----------------------- #
        self.soft_update(self.actor_local, self.actor_target, self.soft_update_tau)
        self.soft_update(self.critic_local, self.critic_target, self.soft_update_tau)

    def save(self, filename):
        torch.save(self.actor_local.state_dict(), 'actor_' + filename)
        torch.save(self.critic_local.state_dict(), 'critic_' + filename)
