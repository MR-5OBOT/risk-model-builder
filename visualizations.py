import random
import matplotlib.pyplot as plt

# Parameters
initial_equity = 5000  # Starting equity
total_trades = 100     # Number of trades
mean_return = 0.01     # Mean return per trade (e.g., 1%)

# Simulate random daily returns
daily_returns = [mean_return + random.uniform(-0.01, 0.02) for _ in range(total_trades)]

# Calculate equity curve
equity_curve = [initial_equity]
for return_ in daily_returns:
    equity_curve.append(equity_curve[-1] * (1 + return_))

# Plotting
plt.style.use("dark_background")
plt.figure(figsize=(8, 6), dpi=100)
plt.plot(equity_curve, color="white", label="Equity Curve")

# Add vertical lines for P/L
if equity_curve[-1] >= initial_equity:
    plt.vlines(total_trades, initial_equity, equity_curve[-1], color="green", label="P/L")
else:
    plt.vlines(total_trades, equity_curve[-1], initial_equity, color="red", label="P/L")

# Add a horizontal line fo starting equity
plt.hlines(initial_equity, xmin=0, xmax=total_trades, color="orange", label=f"Initial Equity")

plt.title("Flow of an Equity Curve", color="white")
plt.xlabel("Total Trades", color="white")
plt.ylabel("Equity ($)", color="white")

final_equity = equity_curve[-1]
color = "green" if final_equity >= initial_equity else "red"  # Concise conditional
label = f"Final Equity (${final_equity:.2f}) ({'Profit' if final_equity >= initial_equity else 'Loss'})"  # f-string formatting
plt.scatter(total_trades, final_equity, color=color, label=label)

plt.legend()
plt.savefig("my_figure.png")
plt.show()

print(f"Final Equity Value: ${final_equity:.2f}")  # f-string formatting
