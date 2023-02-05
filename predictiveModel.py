import random

import torch
import torch.nn as nn
from torch.nn import functional as F 

#import scenarioInitialiser as SI
#import webScraper as WS

batch_size = 4 # Games in the round
block_size = 8 # How many games are we going to take into account
max_iters = 5000 # How many times we iterate
eval_interval = 500 # How many iterations before estimate loss
learning_rate = 1e-3 
device = 'cuda' if torch.cuda.is_available() else 'cpu'
eval_iters = 20 # How many games do we take when estimating loss
n_embd = 316 # how many dimensions does each game (input) have. May have small dimension for each input of the game
n_head = 4 
n_layer = 6
dropout = 0.2

torch.manual_seed(1337)

# Split the data
"""
    train_data - 1999-2019
    val_data - 2020-2021
    test_data - 2022
"""

# Data loading
"""
    Train & Val - take random games from data split. 
    Test - Run through the 2022 season. 
"""
def get_batch(split):
    data = train_data if split == 'train' else val_data 
    year = random.choice(data)

"""
    Look at distance between prediction and result

    Potentially show the distance between 
"""
@torch.no_grad()
def estimate_loss():
    out = {}
    model.eval()
    for split in ['train', 'val']:
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            X, Y = get_batch(split)
            logits, loss = model(X, Y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out

class Head(nn.Module):
    # One head of self-attention

    """
        Should be very similar
        Change to account that n_embd only took in one input (char) but needs to be for all inputs of the game
    """
    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(n_embd, head_size, bias =False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))

        self.dropout = nn.Dropout(dropout)

    """
        Should be fine as is
    """
    def forward(self, x):
        B,T,C = x.shape
        k = self.key(x) # (B,T,C)
        q = self.query(x) # (B,T,C)
        # compute attention score ("affinities")
        wei = q @ k.transpose(-2,-1) * C**-0.5 # (B,T,C) @ (B,C,T) -> (B,T,T)
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf')) #(B,T,T)
        wei = F.softmax(wei, dim=-1) #(B,T,T)
        wei = self.dropout(wei)
        # perform the weighted aggreation of the values
        v = self.value(x) #(B,T,C)
        out = wei @ v # (B,T,T) @ (B,T,C) -> (B,T,C)
        return out
    
class MultiHeadAttention(nn.Module):
    # Multiple heads of self-attention in parallel

    """
        Should be fine as is
    """
    def __init__(self, num_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
        self.proj = nn.Linear(n_embd, n_embd)
        self.dropout = nn.Dropout(dropout)

    """
        Should be fine as is
    """
    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.dropout(self.proj(out))
        return out 

class FeedFoward(nn.Module):
    # A simple linear layer followed by a non-linearity

    """
        Check n_embd is same for multiple inputs
    """
    def __init__(self, n_embd):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),
            nn.ReLU(),
            nn.Linear(4 * n_embd, n_embd),
            nn.Dropout(dropout),
        )
    
    def forward(self, x):
        return self.net(x)


class Block(nn.Module):
    # Transformer block: communication follwed by computation
    
    """
        Check n_embd is accounted for multiple inputs
    """
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


class BigramLanguageModel(nn.Module):

    """
        embedding table needs to be adjusted.
        Vocab_size & n_embd need to be adjusted
    """
    def __init__(self):
        super().__init__()
        # each token directly reads off the logits for the next token from a lookup table
        self.token_embedding_table = nn.Embedding(vocab_size, n_embd)
        self.position_embedding_table == nn.Embedding(vocab_size, n_embd)
        self.blocks = nn.Sequential(*[Block(n_embd, n_head=n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(n_embd) # final layer norm
        self.lm_head = nn.Linear(n_embd, vocab_size)
    
    """
        Change:
        - Token embedding
        - Position embedding
        - Logits representation
        - Loss calculation
    """
    def forward(self, idx, targets=None):
        B,T = idx.shape

        # idx and targets are both (B,T) tensor of integers
        tok_emb = self.token_embedding_table(idx) #(B,T,C)
        pos_emb = self.position_embedding_table(torch.arange(T, device=device)) #(T,C)
        x = tok_emb + pos_emb # (B,T,C)
        x = self.blocks(x) # (B,T,C)
        x = self.ln_f(x) # (B,T,C)
        logits = self.lm_head(x) # (B,T,vocab_size)

        if targets is None:
            loss = None
        else:
            B,T,C = logits.shape
            logits = logits.view(B*T, C) # Try logits representing probability of the score. 
            targets = targets.view(B*T)
            loss = F.cross_entropy(logits, targets) # Try
    
        return logits, loss
    
    """
        Generate is not the same.
        This is the test phase.
        - Run through each game & round
        - Find the losses for each game
        - Test betting using different metrics:
            - Highest prob
            - Summing prob related to bet being made
    """
    def generate(self, idx, max_new_tokens):
        # idx is (B,T) array of indices in the current context
        for _ in range(max_new_tokens):
            # crop idx to the last block_size tokens
            idx_cond = idx[:, -block_size:]
            # get predictions
            logits, loss = self(idx_cond)
            # focus only on the last time step
            logits = logits[:, -1, :] # becomes (B,C)
            # apply softmax to get probabilities
            probs = F.softmax(logits, dim=-1) # (B,C)
            # sample from the distribution
            idx_next = torch.multinomial(probs, num_samples=1) #(B,1)
            # append the sampled index to the running sequence
            idx = torch.cat((idx, idx_next), dim=1) # (B, T+1)
        return idx 
model = BigramLanguageModel()
m = model.to(device)
# print the number of parameters in the model
print(sum(p.numel() for p in m.paramteres())/1e6, 'M parameters')
print()
context = torch.zeros((1,1), dtype=torch.long, device=device)
print("Initial attempt at generating:")
print(decode(m.generate(context, max_new_tokens=2000)[0].tolist()))
print('\n\n\n')


# crate a PyTorch optimizer
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

for iter in range(max_iters):

    # every once in a while evaluate the loss on train and val sets
    if iter % eval_interval == 0 or iter == max_iters - 1:
        losses = estimate_loss()
        print(f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")
    
    # sample a batch of data
    xb, yb = get_batch('train')

    # evaluate the loss
    logits, loss = model(xb, yb)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()

# generate from the model
context = torch.zeros((1,1), dtype=torch.long, device=device)
print(decode(m.generate(context, max_new_tokens=2000)[0].tolist()))



