# Importing the necessary libraries
import torch
import torch.nn as nn
import torch.nn.functional as F

# Defining some hyperparameters
vocab_size = 10000 # The size of the vocabulary
embed_dim = 768 # The dimension of the word embeddings
num_heads = 12 # The number of attention heads
num_layers = 12 # The number of transformer layers
max_len = 512 # The maximum length of the input sequence

# Defining the GPT model class
class GPT(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_heads, num_layers, max_len):
        super(GPT, self).__init__()
        # Creating the word embeddings layer
        self.embeddings = nn.Embedding(vocab_size, embed_dim)
        # Creating the positional embeddings layer
        self.positional_embeddings = nn.Parameter(torch.randn(1, max_len, embed_dim))
        # Creating the transformer encoder layer
        self.transformer = nn.TransformerEncoderLayer(embed_dim, num_heads)
        # Creating the transformer encoder module
        self.encoder = nn.TransformerEncoder(self.transformer, num_layers)
        # Creating the output layer
        self.linear = nn.Linear(embed_dim, vocab_size)

    def forward(self, x):
        # x is a tensor of shape (batch_size, seq_len) containing the input ids
        # Getting the word embeddings for x
        x = self.embeddings(x) # x is now of shape (batch_size, seq_len, embed_dim)
        # Adding the positional embeddings to x
        x = x + self.positional_embeddings[:, :x.size(1), :] # x is still of shape (batch_size, seq_len, embed_dim)
        # Transposing x to match the expected input shape for the encoder
        x = x.transpose(0, 1) # x is now of shape (seq_len, batch_size, embed_dim)
        # Passing x through the encoder
        x = self.encoder(x) # x is still of shape (seq_len, batch_size, embed_dim)
        # Transposing x back to the original shape
        x = x.transpose(0, 1) # x is now of shape (batch_size, seq_len, embed_dim)
        # Passing x through the output layer
        x = self.linear(x) # x is now of shape (batch_size, seq_len, vocab_size)
        # Returning the logits for each token in the sequence
        return x

# Creating an instance of the GPT model
model = GPT(vocab_size, embed_dim, num_heads, num_layers, max_len)

# Printing the model summary
print(model)