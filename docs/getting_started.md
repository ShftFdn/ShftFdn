# Getting Started with Solana MCP & AI Integration Platform

This guide will help you get started with the Solana MCP & AI Integration Platform, which combines blockchain technology with AI and Model Context Protocol (MCP).

## Prerequisites

- Python 3.9 or higher
- Solana CLI tools
- Node.js 16+ and npm/yarn (for Solana client applications)
- A Solana wallet with some SOL on devnet for testing

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/solana-mcp-ai.git
cd solana-mcp-ai
```

### 2. Set up Python environment

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 3. Set up Solana

Make sure you have the Solana CLI tools installed and configured:

```bash
solana config set --url devnet
solana-keygen new --outfile ~/.config/solana/id.json
solana airdrop 2  # Request SOL from the devnet faucet
```

### 4. Set up environment variables

Create a `.env` file in the root directory with the following content:

```
SOLANA_RPC_URL=https://api.devnet.solana.com
SOLANA_KEYPAIR_PATH=~/.config/solana/id.json
MCP_TOKEN_PROGRAM_ID=Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS
MODEL_REGISTRY_PROGRAM_ID=BPFLoader2111111111111111111111111111111111
```

## Basic Usage

### Running a simple language model

```python
from mcp.model_context import ContextType, ContextMetadata, ModelContext, ModelType
from ai.language_model import create_default_language_model
from ai.model_manager import ModelManager

# Create a model manager and register a language model
manager = ModelManager()
language_model = create_default_language_model()
manager.register_model(language_model)
manager.initialize_model(language_model.model_id)

# Create input context
metadata = ContextMetadata(
    creation_time=time.time(),
    source="user_input",
    version="1.0",
    content_type="text/plain",
)

input_context = ModelContext(
    context_id="example_input",
    context_type=ContextType.TEXT,
    data="What is the Model Context Protocol?",
    metadata=metadata,
    model_type=ModelType.LANGUAGE
)

# Run the model
output_context = manager.run_model(language_model.model_id, input_context)
print(output_context.data)
```

### Registering a model on the blockchain

```python
from utils.blockchain import SolanaConfig, SolanaConnection, ModelRegistryClient
from solana.publickey import PublicKey

# Connect to Solana
config = SolanaConfig(
    rpc_url="https://api.devnet.solana.com",
    keypair_path="~/.config/solana/id.json"
)
connection = SolanaConnection(config)

# Create model registry client
model_registry = ModelRegistryClient(
    connection,
    PublicKey("BPFLoader2111111111111111111111111111111111")
)

# Register a model
model_info = language_model.model_info.to_dict()
tx_sig = model_registry.register_model(language_model.model_id, model_info)
print(f"Model registered with signature: {tx_sig}")
```

## Examples

Check out the examples in the `python/examples` directory for more comprehensive examples, including:

- Blockchain integration example
- Image classification with vision models
- Multimodal AI with MCP

## Next Steps

- Learn more about the Model Context Protocol in the [MCP documentation](docs/mcp.md)
- Explore the Solana programs in the `solana/programs` directory
- Check out the JavaScript/TypeScript clients in `solana/clients`

## Troubleshooting

If you encounter issues with Solana connections:

1. Make sure you have SOL in your wallet on the devnet: `solana balance`
2. Check your Solana configuration: `solana config get`
3. Try requesting an airdrop: `solana airdrop 1`

For Python-related issues:

1. Ensure you're using Python 3.9+: `python --version`
2. Make sure all dependencies are installed: `pip install -e .[dev]`
3. Check the logs in the output directory 