# NoxTrade — an AI crypto trading agent you actually own

**Claude-led. Your keys, your Binance, your machine. One-time price, source included.**

NoxTrade is a self-hosted crypto trading agent that lets Anthropic's Claude make the
trading decisions — running on *your* computer, trading on *your* Binance account,
with the full source code in your hands. No cloud holding your API keys. No monthly
subscription. And an honest, public track record that shows the losing weeks too.

This repository is the documentation and "how it works" — **not** the product itself.
The product (with source code) is a one-time purchase at **[noxtrade.de](https://www.noxtrade.de/en)**.

---

## Why this exists

Most "AI trading bots" are a cloud service that holds your exchange API keys and
charges you every month. That's the opposite of what crypto is supposed to be —
you're handing custody and control to someone else's server.

NoxTrade flips that:

- **You own it.** The source ships with the product. Read exactly what it does before
  you ever run it.
- **You hold the keys.** Bring-your-own-key: your Binance API keys stay on your
  machine and are set up with *withdrawals disabled*. The agent can trade — it can
  never move your money out.
- **It's honest.** The live results are public, and they include the drawdowns. This
  is an experiment with real money, not a highlight reel.
- **You pay once.** No subscription.

## What it is *not*

- ❌ Not a signal group, not managed trading, not investment advice.
- ❌ Not a promise of profit. **Crypto trading is risky and you can lose money.**
- ❌ Not a "get rich" scheme. If anyone sells you guaranteed returns, run.

## How it works (high level)

```
Live market stream  →  Technical indicators  →  Claude decides  →  Your Binance
(Binance WebSocket)    (RSI, MACD, ATR, …)     (BUY/SELL/HOLD +    (spot, BYOK,
                                                 reasoning + risk)   withdrawals OFF)
```

1. A background stream watches USDC pairs for meaningful moves and surfaces them
   immediately (no waiting for a fixed interval).
2. For the active symbols it pulls candles (15m + 4h), the order book and 24h stats,
   and computes a set of technical indicators and candlestick patterns.
3. All of that is handed to **Claude**, which returns a structured decision —
   BUY / SELL / HOLD, a confidence, a position size, a stop-loss and take-profit,
   and the **reasoning** behind it.
4. The agent executes on your Binance account, persists open positions to disk
   (so a restart recovers state), and manages exits mechanically between decisions.
5. **A hard stop-loss is always in place.** Risk limits, position caps and a
   drawdown brake sit underneath every trade.

*(The full strategy internals live in the purchased source — this is the shape, not
the secret sauce.)*

## See it live

<!-- ZAHLEN-ANFANG (erzeugt von tools/readme-zahlen.py — nicht von Hand aendern) -->
Real money, real Binance account, running since **23 June 2026**. Numbers as of
**17 August 2026**:

| | |
|---|---|
| Closed trades | **61** (18 winners — a **30 %** hit rate) |
| Return on the traded capital | **+2.32 %** |
| Holding BTC over the same window | -0.33 % |
| Difference | **+2.65 pp** |
| Currently in cash | **90.2 %** |

A 30 % hit rate is not a bug: average winner **+5.9 %**, average loser **-4.1 %**. The geometry has to carry it, and right now it barely does.
<!-- ZAHLEN-ENDE -->

The full equity curve — vs. simply holding BTC, including the losing stretches —
is public here: **[live results](https://www.noxtrade.de/en/live.html)**.

## Try it without a Binance account

A built-in **demo mode** runs the whole thing on simulated market data. No exchange
account, no keys — just watch how the agent thinks.

## Security model

- **Bring your own key (BYOK).** Your Binance API keys never leave your machine.
- Set the key to **Spot trading ON, Withdrawals OFF**, with an IP allow-list.
  On startup the agent checks your key and **refuses to run if withdrawals are
  enabled** — this protects you even from us.
- **We never take custody of your funds.** There is no NoxTrade cloud holding money.

## Get it

One-time purchase, source code + 12 months of updates, at
**[noxtrade.de](https://www.noxtrade.de/en)**.

Honest note on price: there are excellent *free* open-source bots (Freqtrade,
Hummingbot, OctoBot). Those are frameworks — you write and tune the strategy. NoxTrade
is for people who want it to **work out of the box with an AI making the calls**, with
onboarding, support and a public track record. That's what the one-time price buys —
not the source (that's included for transparency).

## FAQ

**Is this a scam?** Read the code. Run the demo with no keys. Watch the public,
loss-included track record. Then decide.

**Does it make money?** No one can promise that, and we don't. The live numbers —
good and bad — are public. Treat it as an experiment with money you can afford to lose.

**Is my money safe from *you*?** Your keys stay on your machine with withdrawals
disabled. There is no path for us to move your funds.

**Do I need to code?** No. There's a guided installer and a step-by-step setup
(English and German). If you can follow a checklist, you can run it.

---

## Disclaimer

NoxTrade is software, not financial or investment advice. Cryptocurrency trading
carries substantial risk, including the loss of your entire capital. Nothing here is
a recommendation to buy or sell any asset, and past behavior does not indicate future
results. You are solely responsible for your own trading decisions and for complying
with the laws and tax rules of your jurisdiction.

© NoxTrade. Documentation in this repository may be read freely; it does not grant a
license to the NoxTrade product, which is sold separately under its own terms.
