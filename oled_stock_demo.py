import machine
import time
import oled_simple_display as ssd1306
import random

# ========================================================
# 1. HARDWARE CONFIGURATION
# ========================================================
WIDTH = 128
HEIGHT = 64
SDA_PIN = 21
SCL_PIN = 22

# Initialize the I2C bus and the OLED screen helper using your clean library file
i2c = machine.I2C(0, sda=machine.Pin(SDA_PIN), scl=machine.Pin(SCL_PIN))
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# ========================================================
# 2. FINTECH DATA INITIALIZATION
# ========================================================
ticker = "AAPL"
price = 175.50  
historical_prices = []  
MAX_DATA_POINTS = 50   

print("--- Fintech Stock Dashboard Initialized ---")

# ========================================================
# 3. REAL-TIME DATA SIMULATION LOOP
# ========================================================
while True:
    try:
        # Clear the old drawing frame
        oled.fill(0)
        
        # --- MATH: Random Walk Stock Price Simulation ---
        change_pct = random.uniform(-0.015, 0.015)
        price_change = price * change_pct
        price += price_change
        
        # Track price history for the sparkline trend graph
        historical_prices.append(price)
        if len(historical_prices) > MAX_DATA_POINTS:
            historical_prices.pop(0)  
            
        # --- UI LAYOUT PART 1: Upper Ticker Header ---
        oled.text(ticker, 0, 0)
        
        # Format the price string to show exactly 2 decimals
        price_str = f"${price:.2f}"
        oled.text(price_str, 55, 0)
        
        # Horizontal layout rule separator line
        oled.hline(0, 12, WIDTH, 1)
        
        # --- UI LAYOUT PART 2: Trend Sparkline Chart ---
        if len(historical_prices) > 1:
            min_p = min(historical_prices)
            max_p = max(historical_prices)
            price_range = max_p - min_p if max_p != min_p else 1
            
            for i in range(len(historical_prices) - 1):
                # Scale the stock numbers dynamically to fit into pixel positions
                x1 = i * 2
                y1 = int(52 - ((historical_prices[i] - min_p) / price_range) * 35)
                
                x2 = (i + 1) * 2
                y2 = int(52 - ((historical_prices[i+1] - min_p) / price_range) * 35)
                
                oled.line(x1, y1, x2, y2, 1)
                
        # --- UI LAYOUT PART 3: Lower Status Footer ---
        if price_change >= 0:
            oled.text("TREND: BULL (+)", 0, 56)
        else:
            oled.text("TREND: BEAR (-)", 0, 56)
            
        # Push completed frame data to glass screen
        oled.show()
        
        # Tick delay (1 transaction per second)
        time.sleep(1)
        
    except OSError:
        print("Hardware Alert: Loose pins shifted contact! Re-apply finger pressure.")
        time.sleep(1)
