---
title: AI Inbox Env
emoji: 📧
colorFrom: blue
colorTo: purple
sdk: docker
app_file: server/app.py
pinned: false
---

# SmartInbox RL Environment

Unlike traditional spam filters, this environment focuses on sequential decision-making under constraints, making it suitable for training intelligent agents rather than static classifiers.

## Overview

This is an OpenEnv-based reinforcement learning environment that simulates real-world email management.

## Problem

Managing emails is not just classification — it involves prioritization, decision-making, and trade-offs.

Agents must:
- identify spam
- prioritize important emails
- decide when to respond
- avoid wasting time on irrelevant messages

## Environment Design

This environment models a dynamic inbox where:
- multiple emails are processed sequentially
- each action has a cost (time/effort)
- wrong decisions have penalties

## Action Space

- move_to_spam
- respond
- ignore

## Observation Space

Each step provides:
- subject
- body
- sender

## Reward Design

Rewards are shaped to simulate real-world trade-offs:

- Correct classification: +0.7  
- Incorrect decision: -0.4  
- Responding to spam: -0.3  
- Ignoring important email: -0.6  
- Reply cost: -0.1  

All rewards are normalized to (0,1) for stable evaluation.

## Tasks

- Easy → clear signals  
- Medium → ambiguous emails  
- Hard → phishing + mixed intent emails  

## Real-World Impact

This environment can be used to train AI agents for:
- email assistants  
- productivity tools  
- enterprise inbox automation  
