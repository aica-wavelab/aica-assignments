"""
Decoder-only Transformer for melody generation.
Shared across the 'Using Large Models' notebook series (modules 10_1 – 10_4).
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class Head(nn.Module):
    """One masked self-attention head."""

    def __init__(self, n_embd, head_size, sequence_len, dropout):
        super().__init__()
        self.key   = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        self.register_buffer('tril', torch.tril(torch.ones(sequence_len, sequence_len)))
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x)
        q = self.query(x)
        v = self.value(x)
        head_size = q.shape[-1]
        wei = q @ k.transpose(-2, -1) * (head_size ** -0.5)
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf'))
        wei = F.softmax(wei, dim=-1)
        wei = self.dropout(wei)
        return wei @ v


class MultiHeadAttention(nn.Module):
    """Multiple attention heads running in parallel."""

    def __init__(self, n_embd, n_heads, head_size, sequence_len, dropout):
        super().__init__()
        self.heads = nn.ModuleList(
            [Head(n_embd, head_size, sequence_len, dropout) for _ in range(n_heads)]
        )
        self.W0 = nn.Linear(head_size * n_heads, n_embd)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        return self.dropout(self.W0(out))


class FeedForward(nn.Module):
    """Position-wise feed-forward network."""

    def __init__(self, n_embd, dropout):
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
    """One transformer block: multi-head attention + feed-forward + layer norms."""

    def __init__(self, n_embd, n_heads, sequence_len, dropout):
        super().__init__()
        head_size = n_embd // n_heads
        self.sa   = MultiHeadAttention(n_embd, n_heads, head_size, sequence_len, dropout)
        self.ffwd = FeedForward(n_embd, dropout)
        self.ln1  = nn.LayerNorm(n_embd)
        self.ln2  = nn.LayerNorm(n_embd)

    def forward(self, x):
        x = x + self.sa(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x


class TransformerDecoder(nn.Module):
    """Decoder-only transformer for next-token prediction."""

    def __init__(self, vocab_size, sequence_len, n_embd, n_heads, n_blocks, dropout):
        super().__init__()
        self.sequence_len = sequence_len
        self.token_embedding_table    = nn.Embedding(vocab_size, n_embd)
        self.position_embedding_table = nn.Embedding(sequence_len, n_embd)
        self.blocks   = nn.Sequential(
            *[Block(n_embd, n_heads, sequence_len, dropout) for _ in range(n_blocks)]
        )
        self.ln_f    = nn.LayerNorm(n_embd)
        self.lm_head = nn.Linear(n_embd, vocab_size)

    def forward(self, idx):
        B, T = idx.shape
        tok_emb = self.token_embedding_table(idx)
        pos_emb = self.position_embedding_table(torch.arange(T, device=idx.device))
        x = tok_emb + pos_emb
        x = self.blocks(x)
        x = self.ln_f(x)
        return self.lm_head(x)

    def encode(self, idx):
        """Return the final hidden states (before lm_head) — useful for embeddings."""
        B, T = idx.shape
        tok_emb = self.token_embedding_table(idx)
        pos_emb = self.position_embedding_table(torch.arange(T, device=idx.device))
        x = tok_emb + pos_emb
        x = self.blocks(x)
        x = self.ln_f(x)
        return x   # (B, T, n_embd)
