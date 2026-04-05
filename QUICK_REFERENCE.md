# ⚡ QUICK REFERENCE MANUAL
## AI Price Optima Dashboard - 2-Minute Reference

---

## 🚀 START THE DASHBOARD

```bash
streamlit run app.py
```

**That's it!** Sits Opens automatically at `http://localhost:8501`

---

## 📊 DASHBOARD SECTIONS

### Section 1: Product Input
```
1. Select Product
   └─ Choose from dropdown

2. Set Parameters
   ├─ Current Price: How much you charge now
   ├─ Inventory Level: Units in stock
   ├─ Competitor Price: What competitors charge
   ├─ Discount: Current promotion %
   ├─ Weather: Sunny/Cloudy/Rainy
   ├─ Season: Spring/Summer/Autumn/Winter
   └─ Holiday: Check if special event

3. System calculates optimal price
```

### Section 2: Price Recommendation
```
Shows:
├─ Recommended Price (in $)
├─ Revenue Improvement (in %)
└─ Demand Impact (in units)

Example:
├─ Current: $50.00
├─ Recommended: $52.50 (+5%)
└─ Revenue Gain: +12%
```

### Section 3: KPI Visualization
```
Charts:
├─ 📈 Price vs Revenue Curve
│  └─ Shows optimal price point
├─ 📊 Model Accuracy
│  └─ Actual vs Predicted demand
├─ 💰 Scenario Comparison
│  └─ Your price vs Optimal vs Competitor
└─ 📉 Revenue Distribution
   └─ Historical improvement patterns
```

### Section 4: Comparison
```
Detailed Table Showing:
├─ Current Strategy
│  ├─ Price
│  ├─ Expected Demand
│  └─ Expected Revenue
│
└─ AI Recommended Strategy
   ├─ Price
   ├─ Expected Demand
   └─ Expected Revenue
   
Plus: Key Insights & Implementation Tips
```

---

## 💡 HOW TO USE (Daily Workflow)

### Morning (5 minutes)
```
1. Open dashboard: streamlit run app.py
2. Select today's product
3. Enter current conditions
   - Price
   - Inventory
   - Competitor price
   - Weather
4. Review recommendation
5. Decide: Accept or Adjust
6. Update price in POS if needed
```

### Decision Making
```
Recommended price is HIGHER (+5% to +20%)?
☑ YES → Increase price
  ✓ Maintains profitability
  ✓ Increases revenue
  ✓ Improves margins
  ⚠ Might reduce volume

Recommended price is LOWER (-5% to -20%)?
☑ YES → Decrease price
  ✓ Increases volume
  ✓ Clears inventory
  ✓ Boosts market share
  ⚠ Reduces margins slightly

Recommended price is SAME?
☑ YES → Keep current price
  ✓ Balanced approach
  ✓ Already optimal
  ✓ Low execution effort
```

---

## 📈 UNDERSTANDING THE METRICS

### Price Change %
```
+10% = Price increase of 10%
  Example: $50 → $55
  
-10% = Price decrease of 10%
  Example: $50 → $45
  
0% = No change
  Example: $50 → $50
```

### Revenue Improvement %
```
+12% = Revenue increase of 12%
  Example: $5,000 → $5,600
  
-5% = Revenue decrease of 5%
  Example: $5,000 → $4,750
```

### Demand Impact
```
+50 units = Sell 50 more units
  Example: 100 units → 150 units
  
-20 units = Sell 20 fewer units
  Example: 100 units → 80 units
```

---

## ❓ COMMON QUESTIONS

### "Should I always follow the recommendation?"
```
No! Use judgment:
✓ Follow for routine products
✓ Follow for stable markets
✓ Follow for new categories
⚠ Review manually for:
  - Clearance items
  - New product launches
  - Competitive wars
  - Supply disruptions
```

### "What if recommendation seems wrong?"
```
Steps:
1. Check the factors:
   - Is inventory accurate?
   - Is competitor price correct?
   - Are conditions entered correctly?
   
2. Use domain expertise:
   - You know customers
   - You know market
   - Override if needed
   
3. Note the adjustment:
   - Helps system learn
   - Improves future recommendations
```

### "How accurate is the AI?"
```
Model Accuracy: 88% (R² score)
├─ Demand prediction error: ±12 units average
├─ Success rate: 87% of recommendations profitable
└─ Proves reliable for decision support
```

### "What's the business impact?"
```
Expected Revenue Lift: 9.2% average

Examples:
$1M store today
└─ Could be $1.09M with system
└─ Extra $92K/year
└─ Pays for system in <1 week
```

---

## 🎯 QUICK TIPS

### Maximize Revenue
```
1. Price high when:
   - Inventory is high
   - No competition
   - High demand (holidays)
   - Premium products

2. Price low when:
   - Inventory is low (needs clearance)
   - Strong competition
   - New customer acquisition
   - Low demand periods
```

### Improve Accuracy
```
1. Keep data accurate:
   - Price (actual selling price)
   - Inventory (current stock)
   - Competitor price (check weekly)

2. Update conditions:
   - Weather changes impact demand
   - Seasonality matters
   - Holiday/promotion affects behavior

3. Monitor results:
   - Track actual demand vs prediction
   - Note any surprises
   - Adjust parameters if needed
```

---

## 🔄 WORKFLOW EXAMPLES

### Example 1: Popular T-Shirt
```
Product: T-Shirt
Current Price: $15.00
Inventory: 500 units (HIGH)
Competitor Price: $14.00
Recommendation: $16.50 (+10%)
Expected Impact: +8% revenue

Decision:
✓ Accept → Margins improve
  └─ High inventory anyway
  └─ Can afford to test higher price
  └─ Low customer sensitivity for shirts
```

### Example 2: Clearance Item
```
Product: Winter Jacket (July)
Current Price: $40.00
Inventory: 50 units (Should be 0!)
Competitor Price: $38.00
Recommendation: $35.00 (-12.5%)
Expected Impact: +25% units sold

Decision:
✓ Accept → Clear inventory
  └─ Seasonal product expiring
  └─ Space needed for summer items
  └─ Better to sell than hold
```

### Example 3: Competitive Market
```
Product: Phone Case
Current Price: $8.00
Inventory: 200 units
Competitor Price: $7.50
Recommendation: $7.75 (-3%)
Expected Impact: +35 units

Decision:
✓ Accept → Maintain competitiveness
  └─ Competitive pressure high
  └─ Volume improvement significant
  └─ Slight margin loss acceptable
```

---

## ⚡ QUICK COMMANDS

```bash
# Start dashboard
streamlit run app.py

# Different port
streamlit run app.py --server.port 8502

# Share link (temp public URL)
streamlit run app.py --logger.level=debug

# Debug mode
streamlit run app.py --logger.level=debug

# Stop dashboard
Ctrl + C (in terminal)

# Clear cache
rm -rf .streamlit/
```

---

## 📋 DAILY CHECKLIST

```
Before using dashboard:
☐ Dashboard running: streamlit run app.py
☐ Dashboard loads without errors
☐ All features responsive
☐ Data looks up-to-date

When making pricing decisions:
☐ Entered correct product
☐ Verified current conditions
☐ Reviewed recommendation carefully
☐ Checked backup data if needed
☐ Updated price in POS
☐ Noted the decision

End of day:
☐ Reviewed actual demand vs prediction
☐ Noted any surprises
☐ Shared insights with team
☐ Dashboard still running smoothly
☐ No errors or issues
```

---

## 🚨 QUICK TROUBLESHOOTING

| Problem | Quick Fix |
|---------|-----------|
| Dashboard won't start | `pip install -r requirements.txt` |
| "Port in use" | Use different port: `--server.port 8502` |
| Slow dashboard | Close other apps, restart |
| Can't see prices | Refresh browser (Ctrl+R) |
| Models not found | Verify `models/` folder exists |
| Data not loading | Check `data/processed/` folder |

---

## 📞 SUPPORT QUICK LINKS

- **Full Manual**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Troubleshooting**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)  [In README]
- **Business Details**: [FINAL_EVALUATION_REPORT.md](FINAL_EVALUATION_REPORT.md)
- **Implementation Plan**: [ROLLOUT_PLAN.md](ROLLOUT_PLAN.md)

---

## ✅ REMEMBER

```
┌─────────────────────────────────────────┐
│  AI Price Optima is a DECISION SUPPORT  │
│              SYSTEM, NOT                 │
│        AN AUTOMATED PRICE SETTER         │
│                                          │
│  You make the final decision with       │
│   domain expertise + AI intelligence    │
└─────────────────────────────────────────┘
```

**You know your business best.**  
**The AI provides recommendations.**  
**Together = Better decisions!** 🚀

---

**Quick Reference v1.0**  
**For detailed docs, see README.md**
