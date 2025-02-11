import random
import matplotlib.pyplot as plt

prop_rules = {
        "max_daily_drawdown": 0.05,  # 5%
        "max_overall_drawdown": 0.10,  # 10%
        "profit_target": 0.10,  # 10%
        # "min_trading_days": 10,
        "risk_per_trade": 0.01,  # 1%
        }

trader_inputs = {
        "win_rate": 0.60,  # 60%
        "reward_to_risk": 2.0,  # 2:1
        "trades_to_pass": 20,  # the user want x trades to pass teh challenge
        }


def adjust_risk(current_balance, initial_balance, current_risk, baseline_risk):
    # Increase risk
    if current_balance >= initial_balance * 1.03:
        return min(current_risk + 0.005, 0.02)  # Cap risk at 5%
    
    # Reduce risk 
    if current_balance <= initial_balance * 0.98:
        return max(current_risk - 0.005, 0.005)  # Floor risk at 0.5%
    
    # Reset risk to baseline if balance returns to initial
    if current_balance >= initial_balance:
        return baseline_risk
    
    return current_risk


def simulate_trades(prop_rules, trader_inputs, num_simulations=100):
    results = []
    for sim in range(num_simulations):
        virtual_balance = 1.0  # Starting balance
        current_risk = prop_rules["risk_per_trade"]
        baseline_risk = prop_rules["risk_per_trade"]
        daily_drawdown = 0
        overall_drawdown = 0
        trades_per_day = 1  # Define a "day" as 5 trades
        simulation_data = {
            "balances": [virtual_balance],
            "risks": [current_risk],
            "drawdowns": [0],
        }

        for trade in range(trader_inputs["trades_to_pass"]):
            # Simulate trade outcome
            if random.random() < trader_inputs["win_rate"]:
                virtual_balance += trader_inputs["reward_to_risk"] * current_risk
            else:
                virtual_balance -= current_risk

            # Adjust risk based on account performance
            current_risk = adjust_risk(virtual_balance, 1.0, current_risk, baseline_risk)

            # Track drawdowns
            daily_drawdown = max(daily_drawdown, 1 - virtual_balance)
            overall_drawdown = max(overall_drawdown, 1 - virtual_balance)

            # Check for daily drawdown violation
            if daily_drawdown >= prop_rules["max_daily_drawdown"]:
                break

            # Reset daily drawdown after a "day" (e.g., 5 trades)
            if (trade + 1) % trades_per_day == 0:
                daily_drawdown = 0

            # Check for overall drawdown violation
            if overall_drawdown >= prop_rules["max_overall_drawdown"]:
                break

            # Track intermediate states
            simulation_data["balances"].append(virtual_balance)
            simulation_data["risks"].append(current_risk)
            simulation_data["drawdowns"].append(overall_drawdown)

        results.append(simulation_data)
    return results


def calculate_metrics(results):
    profit_target = prop_rules["profit_target"]
    passing_simulations = sum(1 for data in results if data["balances"][-1] >= profit_target)
    probability_of_passing = passing_simulations / len(results)
    max_drawdown = max(max(data["drawdowns"]) for data in results)
    return {
        "probability_of_passing": probability_of_passing,
        "max_drawdown": max_drawdown,
    }

# plotting
def plotting(results):
    plt.style.use("dark_background")
    plt.figure(figsize=(8, 5))

    for i, data in enumerate(results):
        # plt.subplot(3, 1, 1)
        plt.plot(data["balances"], label=f"Sim {i+1}")
        plt.axhline(1.10, color="green", linestyle="--", label="Profit Target (10%)")
        plt.axhline(0.90, color="red", linestyle="--", label="Max Drawdown (10%)")
        plt.xlabel("Trade")
        plt.ylabel("Account Balance")
        plt.title("Account Balance Over Time")

        # plt.subplot(3, 1, 2)
        # plt.plot(data["risks"], label=f"Sim {i+1}")
        # plt.xlabel("Trade")
        # plt.ylabel("Risk Level")
        # plt.title("Risk Level Over Time")
        #
        # plt.subplot(3, 1, 3)
        # plt.plot(data["drawdowns"], label=f"Sim {i+1}")
        # plt.xlabel("Trade")
        # plt.ylabel("Drawdown")
        # plt.title("Drawdown Over Time")

    # plt.tight_layout()
    plt.show()


results = simulate_trades(prop_rules, trader_inputs, num_simulations=10)
metrics = calculate_metrics(results)
print("Metrics:", metrics)
plotting(results)
