
#Prediction for the correct score
import csv
import random
import pandas as PD
import numpy as NP

import torch
import torch.nn as nn
from torch.nn import functional as F

import headings as HEAD
import Classes as C

torch.manual_seed(3)
random.seed(3)

batch_size = 4
context_len = 3
game_input_size = 47
attention_layer_size = 47
output_size = 2
dropout = 0.2
block_size = 8
n_layer = 6
n_head = 4
learning_rate = 1e-3
max_iters = 5000
eval_interval = 500
device = 'cuda' if torch.cuda.is_available() else 'cpu'

val_year = 2021
test_year = 2022

games = []
train_games = [[] for _ in range(8)]
val_games = [[]]
test_games = [[]]

data = PD.read_csv('gameDataV2.csv')
data_arr = data.to_numpy().tolist()

team_names = set()
num_errors = 0
for game in data_arr:
    if game[2] not in team_names:
        team_names.add(game[2])
    if game[3] not in team_names:
        team_names.add(game[3])
    if game[2] == 'points' or game[3] == 'points' or game[2] == 'away Team' or game[3] == 'away Team':
        num_errors += 1
    #if game[2] == 'away Team' or game[3] == 'away Team':

teams = []
for name in team_names:
    teams.append(C.Team(name))


for game in data_arr:
    year = game[0]
    round = game[1]
    if year == 2022:
        if len(test_games[0]) == 0:
            test_games[0] = [[game]]
        else:
            if round == test_games[0][-1][-1][1]:
                test_games[0][-1].append(game)
            else:
                if round == test_games[0][-1][-1][1] + 1:
                    test_games[0].append([game])
                else:
                    test_games[0].append([0 for _ in range(len(game))])
                    test_games[0].append([game])
    else:
        if year == 2021:
            if len(val_games[0]) == 0:
                val_games[0] = [[game]]
            else:
                if round == val_games[0][-1][-1][1]:
                    val_games[0][-1].append(game)
                else:
                    if round == val_games[0][-1][-1][1]:
                        val_games[0][-1].append(game)
                    val_games[0].append([game])
        else:
            if len(train_games[year-2013]) == 0:
                train_games[year-2013] = [[game]]
                continue 
            prev_game = train_games[year-2013][-1]
            if len(prev_game) == 0:
                train_games[year-2013].append(game)
            else:
                if train_games[year-2013][-1][-1][1]== round:
                    train_games[year-2013][-1].append(game)
                else:
                    train_games[year-2013].append([game])
    round = game[1]
    score = [game[4], game[5]]
    for team in teams:
        if team.name == game[2]:
            if year < val_year:
                team.train_games[year-2013].append(HEAD.get_team_data('home', game))
                team.train_scores[year-2013].append(score)
                team.train_opponent[year-2013].append(game[3])
            if year == val_year:
                team.val_games.append(HEAD.get_team_data('home', game))
                team.val_scores.append(score)
                team.val_opponent.append(game[3])
            if year == test_year:
                team.test_games.append(HEAD.get_team_data('home', game))
                team.test_scores.append(score)
                team.test_opponent.append([game[3]])
        else:
            if team.name == game[3]:
                if year < val_year:
                    team.train_games[year-2013].append(HEAD.get_team_data('away', game))
                    team.train_scores[year-2013].append(score)
                    team.train_opponent[year-2013].append(game[2])
                if year == val_year:
                    team.val_games.append(HEAD.get_team_data('away', game))
                    team.val_scores.append(score)
                    team.val_opponent.append(game[2])
                if year == test_year:
                    team.test_games.append(HEAD.get_team_data('away', game))
                    team.test_scores.append(score)
                    team.test_opponent.append(game[2])


for team in teams:
    team.train_games.pop()
    team.train_games.pop()

print(teams[-1].name)
print(teams[-1].train_games[0][0])
xxxxxx

def batch_data(split):
    if split == 'train':
        # Retrieve random round
        year_games = random.choice(train_games)
        round_games = random.choice(year_games)
        
        year = round_games[0][0]
        round_num = round_games[0][1]
        print(f'Year: {year}')
        print(f'Round number: {round_num}')
        

        # Find context info about each game
        xb = []
        yb = []
        
        for game in round_games:
            
            for team in teams:
                if team.name == game[2]:
                    home_team = team
                if team.name == game[3]:
                    away_team = team

            x_vals = []
            y_vals = [game[4], game[5]]

            # Context data for home team
            for i in range(context_len):
                if round_num - i < 1:
                    for _ in range(len(home_team.train_games[year-2013][0])):
                        x_vals.append(0)
                else:
                    x_vals += home_team.train_games[year-2013][round_num - i - 2]
            # Away team data
            for i in range(context_len):
                if round - i < 1:
                    for _ in range(len(away_team.train_games[year-2013][0])):
                        x_vals.append(0)
                else:
                    x_vals += away_team.train_games[year-2013][round_num - i - 2]
            x_vals = [int(x) for x in x_vals]
            xb.append(torch.tensor(x_vals))
            yb.append(torch.tensor(y_vals))
    X = torch.stack(xb)
    Y = torch.stack(yb)

    X, Y = X.to(device), Y.to(device)
    return X, Y

class Head(nn.Module):
    # One head of self-attention

    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(attention_layer_size, head_size, bias=False)
        self.query = nn.Linear(attention_layer_size, head_size, bias=False)
        self.value = nn.Linear(attention_layer_size, head_size, bias=False)
        self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        B,T,C = x.shape
        k = self.key(x) # (B,T,C)
        q = self.query(x) # (B,T,C)
        # compute attention score ("affinities")
        wei = q @ k.transpose(-2,-1) * C**-0.5 # (B, T, C) @ (B, C, T) -> (B, T, T)
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf')) # (B, T, T)
        wei = F.softmax(wei, dim=-1) # (B, T, T)
        wei = self.dropout(wei)
        # perform the weighted aggregation of the values 
        v = self.value(x) # (B, T, C)
        out = wei @ v # (B, T, T) @ (B, T, C) -> (B, T, C)
        return out 

class MultiHeadAttention(nn.Module):
    # Multiple heads of self-attention in parallel

    def __init__(self, num_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
        self.proj = nn.Linear(attention_layer_size, attention_layer_size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.dropout(self.proj(out))
        return out 

class FeedFoward(nn.Module):
    # A simple linear layer followed by a non-linearity

    def __init__(self, n_embd):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(attention_layer_size, 4 * attention_layer_size),
            nn.ReLU(),
            nn.Linear(4 * attention_layer_size, attention_layer_size),
            nn.Dropout(dropout),
        )

    def forward(self, x):
        return self.net(x)


class Block(nn.Module):
    # Transformer blcok: communication followed by computation

    def __init__(self, n_embd, n_head):
        # n_embd: embedding dimension, n_head: the number of heads we'd like
        super().__init__()
        head_size = n_embd // n_head 
        self.sa = MultiHeadAttention(n_head, head_size)
        self.ffwd = FeedFoward(n_embd)
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)

    def forward(self, x):
        x = x + self.sa(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x 


class PredictionModel(nn.Module):

    def __init__(self):
        super().__init__()
        # each token directly reads off the logits for the next token from a lookup table
        self.token_embedding_table = nn.Linear(context_len*game_input_size, attention_layer_size)
        self.position_embedding_table = nn.Linear(context_len*game_input_size, attention_layer_size)
        self.blocks = nn.Sequential(*[Block(attention_layer_size, n_head=n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(attention_layer_size) # final layer norm
        self.lm_head = nn.Linear(attention_layer_size, output_size)

    def forward(self, idx, targets=None):
        B, T = idx.shape

        # idx and targets are both (B,T) tensor of integers
        tok_emb = self.token_embedding_table(idx) # (B,T,C)
        pos_emb = self.position_embedding_table(torch.arange(T, device=device)) # (T,C)
        x = tok_emb + pos_emb # (B,T,C)
        x = self.blocks(x) # (B,T,C)
        x = self.ln_f(x) # (B,T,C)
        logits = self.lm_head(x) # (B,T,vocab_size)

        if targets is None:
            loss = None
        else:
            B, T, C = logits.shape
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)
            loss = F.cross_entropy(logits, targets)
        
        return logits, loss

print("Pre model")
model = PredictionModel()
print("Between model and m")
m = model.to(device)
# print the number of parameters in the model
print(sum(p.numel() for p in m.parameters())/1e6, 'M parameters')
print()
# run through 2022 and calculate correct predictions and betting outcome


# create a PyTorch optimizer
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

for iter in range(max_iters):

    # every once in a while evaluate the loss on train and val sets
    """
    if iter % eval_interval == 0 or iter == max_iters - 1:
        losses = estimate_loss()
        print(f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")
    """
    # sample a batch of data
    xb, yb = batch_data('train')
    print(xb)
    print(yb)
    xxxxxxx
    # evaluate the loss
    logits, loss = model(xb, yb)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()

# run through 2022 and calculate correct predictions and betting outcome

