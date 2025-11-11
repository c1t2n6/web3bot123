from dotenv import load_dotenv
import os

# Load env and project
load_dotenv()

from bot_template import PortfolioManager

try:
    initial_capital = float(os.getenv('INITIAL_CAPITAL', '50000.0'))
except Exception:
    initial_capital = 50000.0

pm = PortfolioManager(initial_capital)
metrics = pm.get_portfolio_metrics()
print(f"Initial capital: ${pm.initial_capital:,.2f}")
print(f"Current capital: ${pm.current_capital:,.2f}")
print("Metrics:")
for k, v in metrics.items():
    print(f"  {k}: {v}")

