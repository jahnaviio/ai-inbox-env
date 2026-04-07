# AI Inbox Environment (OpenEnv)

## 📌 Overview

AI Inbox Environment is a real-world simulation of email triage, where an AI agent must classify incoming emails and decide appropriate actions such as marking spam, responding to important emails, or handling personal messages.

This environment is designed to evaluate and train AI agents on practical decision-making tasks similar to real email management systems.

---

## 🎯 Motivation

Email overload is a real-world problem. This environment simulates how AI can assist users in:

- Filtering spam emails
- Identifying important communications
- Managing personal conversations

It provides a structured benchmark for evaluating intelligent agents in a realistic domain.

---

## 🧠 Environment Design

The environment follows the OpenEnv standard:

### Core APIs

- `reset()` → Initializes a new email task
- `step(action)` → Processes agent action and returns:
  - observation
  - reward
  - done
  - info
- `state()` → (can be extended)

---

## 📥 Observation Space

Each observation contains:

- `email_id` (int)
- `subject` (str)
- `body` (str)
- `sender` (str)

---

## 🎬 Action Space

Agent outputs an action with:

- `action_type`:
  - `respond`
  - `ignore`
- `label`:
  - `spam`
  - `important`
  - `personal`
- `response_text` (optional)

---

## 🧪 Tasks

### 🟢 Easy
- Clear classification (e.g., meeting emails)
- Straightforward decision

### 🟡 Medium
- Mix of spam and personal emails
- Requires better keyword understanding

### 🔴 Hard
- Ambiguous emails
- Requires contextual reasoning

---

## 🏆 Reward Function

The environment provides **dense rewards**:

- `1.0` → correct classification
- `0.5` → partially correct (important vs personal confusion)
- `0.0` → incorrect (especially spam mistakes)

This allows agents to learn progressively rather than relying on binary success.

---

## 🤖 Baseline Agent

A deterministic rule-based agent is provided:

- Uses keyword matching
- Produces consistent and reproducible results
- Runs within required time constraints

---

## 📊 Baseline Results

| Task   | Score |
|--------|------|
| Easy   | 1.00 |
| Medium | 0.50–1.00 |
| Hard   | 0.50–1.00 |

---

## ⚙️ Setup Instructions

```bash
pip install -r requirements.txt