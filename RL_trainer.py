from collections import OrderedDict
from environments import CartPoleEnv
from algorithms import (
    DQN_Agent,
    SARSA_Agent,
    SARSALambda_Agent,
    ActorCritic_Agent,
    A2C_Agent,
    PPO_Agent,
)
# from dev import (
#     A3C_Agent,
#     TRPO_Agent,
# )
from models import SimpleModel
import torch.optim as optim
import argparse


class RLTrainer:
    def __init__(self, model, optimizer, env, config):
        self.env = env
        self.model = model
        self.config = config
        self.optimizer = optimizer
        self.lr = config['optimizer_args']['lr']
        self.algorithm = self._get_algorithm(config['algorithm_name'])
    
    def _get_algorithm(self, algorithm_name):
        return globals()[algorithm_name + "_Agent"](self.model, self.optimizer, self.env, **self.config)

    def train(self):
        self.algorithm.train(**self.config['train_args'], n=self.env.action_space)

    def test(self):
        self.algorithm.test(**self.config['test_args'])

    def run(self):
        self.test()
        self.train()
        self.test()

def main(args):
    env = CartPoleEnv()

    config = OrderedDict(
        algorithm_name = args.algorithm,
        train_args = OrderedDict(
            num_episodes=200,
            batch_size=128,
            gamma=0.999,
            lambda_=0.9,
            eps_clip=0.2,
            gae_lambda=0.95,
            entropy_beta=0.01,
            tau=0.95,
        ),
        test_args = OrderedDict(
            num_episodes=10,
        ),
        optimizer_args = OrderedDict(
            lr=0.001,
            alpha=0.99,
        ),
        model_args = OrderedDict(
            input_size=env.observation_space,
            output_size=env.action_space,
        ),
        decode_args = OrderedDict(
            strategy=args.strategy,
            epsilon_start=0.9,
            epsilon_end=0.05,
            epsilon_decay=200,
            n=env.action_space,
            c=0.5,
            temperature=0.7,
        )
    )

    model = SimpleModel
    optimizer = optim.RMSprop
    trainer = RLTrainer(
        model=model,
        optimizer=optimizer,
        env=env,
        config=config
    )

    trainer.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--algorithm", default="DQN")
    parser.add_argument("--strategy", default="EpsilonGreedy")
    args = parser.parse_args()
    main(args=args)
