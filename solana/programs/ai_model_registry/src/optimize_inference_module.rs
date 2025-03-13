//! optimize_inference_module module for data marketplace
//!
//! This module provides functionality for implementing data marketplace functionality.

use anchor_lang::prelude::*;
use anchor_spl::token::{self, Token, TokenAccount, Mint};

/// OptimizeInferenceModule state account
#[account]
pub struct OptimizeInferenceModule {
    /// The authority that can update this account
    pub authority: Pubkey,
    
    /// Status of the account
    pub status: u8,
    
    /// Additional data
    pub data: [u8; 32],
    
    /// Creation time
    pub created_at: i64,
}

/// Initialize a new OptimizeInferenceModule
pub fn initialize_optimize_inference_module(ctx: Context<InitializeOptimizeInferenceModule>) -> Result<()> {
    let account = &mut ctx.accounts.optimize_inference_module;
    account.authority = ctx.accounts.authority.key();
    account.status = 1; // Active
    account.created_at = Clock::get()?.unix_timestamp;
    
    Ok(())
}

/// Update OptimizeInferenceModule data
pub fn update_optimize_inference_module(ctx: Context<UpdateOptimizeInferenceModule>, data: [u8; 32]) -> Result<()> {
    let account = &mut ctx.accounts.optimize_inference_module;
    account.data = data;
    
    Ok(())
}

/// Account validation
#[derive(Accounts)]
pub struct InitializeOptimizeInferenceModule<'info> {
    /// The authority that can update this account
    #[account(mut)]
    pub authority: Signer<'info>,
    
    /// The account to initialize
    #[account(
        init,
        payer = authority,
        space = 8 + 32 + 1 + 32 + 8,
    )]
    pub optimize_inference_module: Account<'info, OptimizeInferenceModule>,
    
    /// System program
    pub system_program: Program<'info, System>,
}

/// Account validation for update
#[derive(Accounts)]
pub struct UpdateOptimizeInferenceModule<'info> {
    /// The authority that can update this account
    #[account(mut)]
    pub authority: Signer<'info>,
    
    /// The account to update
    #[account(
        mut,
        constraint = optimize_inference_module.authority == authority.key()
    )]
    pub optimize_inference_module: Account<'info, OptimizeInferenceModule>,
}
