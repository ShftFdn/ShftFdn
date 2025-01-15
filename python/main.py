"""
Main application entry point for the Solana MCP & AI Integration Platform.

This module provides a CLI and integration points for the MCP, AI models,
and Solana blockchain components.
"""
import argparse
import json
import logging
import os
import sys
import time
import uuid
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from solana.publickey import PublicKey

from mcp.model_context import (
    ContextMetadata, 
    ContextRegistry, 
    ContextType, 
    ModelContext, 
    ModelType
)
from ai.model_manager import ModelManager, ModelStatus
from ai.language_model import create_default_language_model
from utils.blockchain import (
    SolanaConfig, 
    SolanaConnection, 
    MCPTokenClient, 
    ModelRegistryClient
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("solana_mcp_ai.log")
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def setup_solana_connection() -> SolanaConnection:
    """Set up connection to Solana blockchain."""
    # Modified: 2025-04-26T22:17:04.784146
    rpc_url = os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com")
    keypair_path = os.getenv("SOLANA_KEYPAIR_PATH")
    
    if not keypair_path:
        logger.warning("No keypair path provided. Using ephemeral keypair.")
        keypair_path = None
    
    config = SolanaConfig(
        rpc_url=rpc_url,
        keypair_path=keypair_path
    )
    
    return SolanaConnection(config)


def setup_model_manager() -> ModelManager:
    """Set up the AI model manager."""
    manager = ModelManager()
    
    # Register default language model
    language_model = create_default_language_model()
    manager.register_model(language_model)
    
    return manager


def setup_context_registry() -> ContextRegistry:
    """Set up the context registry."""
    return ContextRegistry()


def run_text_generation(manager: ModelManager, 
                      registry: ContextRegistry, 
                      input_text: str) -> Optional[str]:
    """Run text generation using the language model."""
    # Create input context
    context_id = f"text_input_{uuid.uuid4().hex[:8]}"
    metadata = ContextMetadata(
        creation_time=time.time(),
        source="user_input",
        version="1.0",
        content_type="text/plain",
    )
    
    input_context = ModelContext(
        context_id=context_id,
        context_type=ContextType.TEXT,
        data=input_text,
        metadata=metadata,
        model_type=ModelType.LANGUAGE
    )
    
    # Register the input context
    registry.register(input_context)
    
    # Find a suitable language model
    models = manager.list_models(model_type=ModelType.LANGUAGE)
    if not models:
        logger.error("No language models available")
        return None
    
    # Use the first available model
    model_id = models[0].model_id
    
    # Initialize the model if needed
    model = manager.get_model(model_id)
    if model.status == ModelStatus.INITIALIZING:
        logger.info(f"Initializing model {model_id}")
        if not manager.initialize_model(model_id):
            logger.error(f"Failed to initialize model {model_id}")
            return None
    
    # Run the model
    logger.info(f"Running model {model_id}")
    output_context = manager.run_model(model_id, input_context)
    if not output_context:
        logger.error(f"Failed to run model {model_id}")
        return None
    
    # Register the output context
    registry.register(output_context)
    
    return output_context.data


def register_model_on_chain(connection: SolanaConnection, 
                          model_registry: ModelRegistryClient,
                          model_id: str,
                          model_info: Dict[str, Any]) -> Optional[str]:
    """Register a model on the blockchain."""
    logger.info(f"Registering model {model_id} on the blockchain")
    return model_registry.register_model(model_id, model_info)


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="Solana MCP & AI Integration Platform"
    )
    parser.add_argument(
        "--action",
        choices=["generate", "register", "list"],
        default="generate",
        help="Action to perform"
    )
    parser.add_argument(
        "--input",
        help="Input text for generation"
    )
    parser.add_argument(
        "--model-id",
        help="Model ID for registration"
    )
    args = parser.parse_args()
    
    # Set up components
    try:
        solana_connection = setup_solana_connection()
        model_manager = setup_model_manager()
        context_registry = setup_context_registry()
    except Exception as e:
        logger.exception(f"Error setting up components: {str(e)}")
        return
    
    # Create clients
    try:
        mcp_token_client = MCPTokenClient(
            solana_connection,
            PublicKey(os.getenv("MCP_TOKEN_PROGRAM_ID", "Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS")),
            PublicKey(os.getenv("MCP_TOKEN_MINT", "4uQeVj5tqViQh7yWWGStvkEG1Zmhx6uasJtWCJziofM"))
        )
        model_registry_client = ModelRegistryClient(
            solana_connection,
            PublicKey(os.getenv("MODEL_REGISTRY_PROGRAM_ID", "BPFLoader2111111111111111111111111111111111"))
        )
    except Exception as e:
        logger.exception(f"Error creating clients: {str(e)}")
        return
    
    # Perform action
    if args.action == "generate":
        if not args.input:
            logger.error("No input text provided")
            return
        
        output = run_text_generation(model_manager, context_registry, args.input)
        if output:
            logger.info(f"Generated text: {output}")
    
    elif args.action == "register":
        if not args.model_id:
            logger.error("No model ID provided")
            return
        
        models = model_manager.list_models()
        model_info = None
        
        for model in models:
            if model.model_id == args.model_id:
                model_info = model.to_dict()
                break
        
        if not model_info:
            logger.error(f"Model {args.model_id} not found")
            return
        
        tx_sig = register_model_on_chain(
            solana_connection,
            model_registry_client,
            args.model_id,
            model_info
        )
        
        if tx_sig:
            logger.info(f"Model registered on chain: {tx_sig}")
        else:
            logger.error("Failed to register model on chain")
    
    elif args.action == "list":
        models = model_manager.list_models()
        logger.info(f"Available models: {len(models)}")
        for model in models:
            logger.info(f"  - {model.model_id}: {model.name} ({model.status.value})")


if __name__ == "__main__":
    main() 