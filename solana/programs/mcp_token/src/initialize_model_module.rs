//! initialize_model_module module for data marketplace
//!
//! This module provides functionality for implementing data marketplace functionality.

use anchor_lang::prelude::*;
use anchor_spl::token::{self, Token, TokenAccount, Mint};

/// InitializeModelModule state account
#[account]
pub struct InitializeModelModule {
    /// The authority that can update this account
    pub authority: Pubkey,
    
    /// Status of the account
    pub status: u8,
    
    /// Additional data
    pub data: [u8; 32],
    
    /// Creation time
    pub created_at: i64,
}

/// Initialize a new InitializeModelModule
pub fn initialize_initialize_model_module(ctx: Context<InitializeInitializeModelModule>) -> Result<()> {
    let account = &mut ctx.accounts.initialize_model_module;
    account.authority = ctx.accounts.authority.key();
    account.status = 1; // Active
    account.created_at = Clock::get()?.unix_timestamp;
    
    Ok(())
}

/// Update InitializeModelModule data
pub fn update_initialize_model_module(ctx: Context<UpdateInitializeModelModule>, data: [u8; 32]) -> Result<()> {
    let account = &mut ctx.accounts.initialize_model_module;
    account.data = data;
    
    Ok(())
}

/// Account validation
#[derive(Accounts)]
pub struct InitializeInitializeModelModule<'info> {
    /// The authority that can update this account
    #[account(mut)]
    pub authority: Signer<'info>,
    
    /// The account to initialize
    #[account(
        init,
        payer = authority,
        space = 8 + 32 + 1 + 32 + 8,
    )]
    pub initialize_model_module: Account<'info, InitializeModelModule>,
    
    /// System program
    pub system_program: Program<'info, System>,
}

/// Account validation for update
#[derive(Accounts)]
pub struct UpdateInitializeModelModule<'info> {
    /// The authority that can update this account
    #[account(mut)]
    pub authority: Signer<'info>,
    
    /// The account to update
    #[account(
        mut,
        constraint = initialize_model_module.authority == authority.key()
    )]
    pub initialize_model_module: Account<'info, InitializeModelModule>,
}
