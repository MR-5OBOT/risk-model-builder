import logging
import random

import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)  # Set logging level

# User inputs
# max_daily_drawdown = float(input("Enter max daily drawdown (e.g., 0.05 for 5%): "))
# max_overall_drawdown = float(input("Enter max overall drawdown (e.g., 0.10 for 10%): "))
# profit_target = float(input("Enter profit target (e.g., 0.10 for 10%): "))
# risk_per_trade = float(input("Enter risk per trade (e.g., 0.01 for 1%): "))
#
# win_rate = float(input("Enter win rate (e.g., 0.60 for 60%): "))
# reward_to_risk = float(input("Enter reward to risk ratio (e.g., 2.0 for 2:1): "))
# trades_to_pass = int(input("Enter number of trades needed to pass: "))

max_daily_drawdown = 0.03
max_overall_drawdown = 0.6
profit_target = 0.6
risk_per_trade = 0.01

win_rate = 0.55
reward_to_risk = 2.0  # 2:1 RR
trades_to_pass = 20  # Example number of trades needed to pass

initial_balance = 50000


def adjust_risk(current_balance, current_risk, baseline_risk):
    if current_balance >= initial_balance * random.uniform(0.01, 0.03):
        return min(current_risk + 0.005, 0.02)
    if current_balance <= initial_balance * random.uniform(-0.01, -0.02):
        return max(current_risk - 0.005, 0.005)
    if current_balance >= initial_balance:
        return baseline_risk
    return current_risk


def simulate_trades(num_simulations=100):
    results = []
    for sim in range(num_simulations):
        virtual_balance = initial_balance
        current_risk = risk_per_trade
        baseline_risk = risk_per_trade
        daily_drawdown = 0
        overall_drawdown = 0
        simulation_data = {
            "balances": [virtual_balance],
            "risks": [current_risk],
            "drawdowns": [0],
        }

        for trade in range(trades_to_pass):
            if random.random() < win_rate:
                virtual_balance += reward_to_risk * current_risk
                # logging.info("winning trade!")
            else:
                virtual_balance -= current_risk
                # logging.info("lossing trade!")

            current_risk = adjust_risk(virtual_balance, current_risk, baseline_risk)
            daily_drawdown = max(daily_drawdown, initial_balance - virtual_balance)
            overall_drawdown = max(overall_drawdown, initial_balance - virtual_balance)

            if daily_drawdown >= max_daily_drawdown:
                # logging.info("daily_drawdown reached!")
                break
            elif overall_drawdown >= max_overall_drawdown:
                # logging.info("overall_drawdown reached!")
                break
            # target check
            elif virtual_balance == profit_target:
                logging.info("target reached!")
                break

            simulation_data["balances"].append(virtual_balance)
            simulation_data["risks"].append(current_risk)
            simulation_data["drawdowns"].append(overall_drawdown)

        results.append(simulation_data)

        # convert floats
        daily_drawdown = daily_drawdown * 100
        overall_drawdown = overall_drawdown * 100
        baseline_risk = baseline_risk * 100

        logging.info(f"[Simulation] Current virtual_balance: {virtual_balance}%")
        logging.info(f"[Simulation] daily_drawdown: {daily_drawdown}%")
        logging.info(f"[Simulation] overall_drawdown: {overall_drawdown}%")
        logging.info(f"[Simulation] baseline_risk: {baseline_risk}%")
    return results


def plotting(results):
    plt.style.use("dark_background")
    plt.figure(figsize=(8, 5))

    for i, data in enumerate(results):
        plt.plot(data["balances"], label=f"Sim {i+1}")
        plt.legend()
        plt.axhline(
            profit_target + profit_target,
            color="green",
            linestyle="--",
            label="Profit Target",
        )
        plt.axhline(
            initial_balance - max_overall_drawdown,
            color="red",
            linestyle="--",
            label="Max Drawdown",
        )
        plt.xlabel("Trade")
        plt.ylabel("Account Balance")
        plt.title("Account Balance Over Time")

    plt.show()


results = simulate_trades(num_simulations=10)
# plotting(results)
