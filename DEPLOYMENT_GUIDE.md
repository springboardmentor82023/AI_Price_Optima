# 🚀 DEPLOYMENT GUIDE
## AI Price Optima - Dashboard Deployment Instructions

**Quick Deploy**: 5 minutes  
**Full Setup**: 15 minutes  
**Tested On**: Windows, macOS, Linux  

---

## 🎯 Quick Start (Fastest Way)

### For Windows
```bash
# 1. Open PowerShell in the project folder
# 2. Run:
pip install -r requirements.txt
python -m streamlit run app.py
```

### For macOS/Linux
```bash
# 1. Open Terminal in the project folder
# 2. Run:
pip install -r requirements.txt
python -m streamlit run app.py
```

**Result**: Dashboard opens in browser at `http://localhost:8501`

---

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **pip**: Python package manager (comes with Python)
- **Internet**: Needed for initial setup
- **RAM**: 2GB minimum
- **Storage**: 500MB available space

### Check Prerequisites
```bash
# Check Python version
python --version

# Should show: Python 3.8.x or higher
```

If Python is not installed:
1. Go to https://www.python.org/
2. Download Python 3.10+ LTS
3. Install with "Add Python to PATH" ✓
4. Restart terminal

---

## 🔧 Installation Options

### Option 1: Simple Installation (Recommended)
```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

### Option 2: Virtual Environment (Best Practice)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Run dashboard
streamlit run app.py
```

### Option 3: Docker (Advanced)
```bash
# Build Docker image
docker build -t ai-price-optima .

# Run container
docker run -p 8501:8501 ai-price-optima

# Access at: http://localhost:8501
```

---

## 🎮 Running the Dashboard

### Standard Launch
```bash
streamlit run app.py
```

### Launch with Custom Port
```bash
streamlit run app.py --server.port 8502
```

### Launch in Headless Mode
```bash
streamlit run app.py --server.headless true
```

### Full Command Reference
```bash
# Enable debug logging
streamlit run app.py --logger.level=debug

# Set theme
streamlit run app.py --theme.base="dark"

# Disable browser auto-open
streamlit run app.py --client.showErrorDetails=false
```

---

## 📱 Accessing the Dashboard

### Local Access
- **URL**: `http://localhost:8501`
- **From same computer**: Click the auto-opened link

### Remote Access (from another computer)
1. Find your computer's IP address:
   ```bash
   # Windows PowerShell
   ipconfig
   # Look for "IPv4 Address"
   
   # macOS/Linux
   ifconfig
   # Look for "inet"
   ```

2. Access from other computer:
   ```
   http://<YOUR_IP>:8501
   ```

### Network Share (Advanced)
```bash
# Allow external connections
streamlit run app.py --server.address=0.0.0.0
```

---

## ⚙️ Configuration

### Edit Streamlit Config (if needed)
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
maxUploadSize = 200
port = 8501
headless = false
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit
# Or reinstall all:
pip install -r requirements.txt
```

### "Address already in use" / "Port 8501 in use"
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill process using port:
# Windows PowerShell:
Get-Process | Where-Object {$_.ProcessName -match "python"} | Stop-Process -Force

# macOS/Linux:
lsof -i :8501
kill -9 <PID>
```

### "Models or data files not found"
```bash
# Verify file structure:
# Should have:
# ├── models/
# │   ├── xgb_units_sold_model.pkl
# │   └── lgbm_units_sold_model.pkl
# ├── data/processed/
# │   └── retail_store_inventory_cleaned.csv
# └── model_backtesting_results.csv

# If missing, download/restore files
```

### Dashboard shows "Error loading application"
```bash
# Check requirements
pip install --upgrade -r requirements.txt

# Clear cache
rm -rf ~/.streamlit/cache_factory.db

# Restart
streamlit run app.py
```

### Slow loading or timeouts
```bash
# Increase timeout
streamlit run app.py --client.maxMessageSize=200

# Check system resources
top  # or Task Manager on Windows

# Try restarting
```

---

## 📊 Dashboard Features

### Main Sections
1. **Section 1: Product Input**
   - Select product
   - Set current price
   - Adjust inventory level
   - Configure competitor pricing

2. **Section 2: Price Recommendation**
   - Recommended price
   - Revenue improvement %
   - Demand impact

3. **Section 3: KPI Visualization**
   - Price vs Revenue curve
   - Model prediction accuracy
   - Scenario comparison
   - Revenue distribution

4. **Section 4: Comparison**
   - Current vs Recommended
   - Detailed metrics table
   - Key insights
   - Implementation recommendations

---

## 🔄 Data Refresh

### Auto-Refresh (Default)
- Dashboard refreshes on every interaction
- No manual reload needed
- Caches data for performance

### Manual Refresh
- **Press**: Ctrl+R (browser refresh)
- **Or**: Click browser refresh button

### Clear Cache (if needed)
```bash
# Clear Streamlit cache
rm -rf .streamlit/

# Restart dashboard
streamlit run app.py
```

---

## 🚀 Production Deployment

### Option 1: Streamlit Cloud (Easiest)
1. Push code to GitHub
2. Go to [https://share.streamlit.io/](https://share.streamlit.io/)
3. Connect GitHub account
4. Select repository
5. Deploy!

### Option 2: Cloud Platforms
- **Heroku**: `git push heroku main`
- **AWS**: Use ECS + Elastic Container Registry
- **Google Cloud**: Cloud Run
- **Azure**: App Service

### Option 3: On-Premise Server
```bash
# 1. Copy project to server
scp -r AI_Price_Optima/ user@server:/app/

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run with systemd (Linux)
[Unit]
Description=AI Price Optima Dashboard
After=network.target

[Service]
Type=simple
User=app-user
WorkingDirectory=/app/AI_Price_Optima
ExecStart=/usr/bin/python -m streamlit run app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

---

## 📈 Monitoring

### Check System Health
```bash
# Monitor resource usage while running
# Windows:
Get-Process python | Select-Object ProcessName, CPU, Memory

# macOS/Linux:
top -p $(pgrep -f streamlit)
```

### View Logs
```bash
# Streamlit logs usually in console
# Check for errors and warnings

# Debug mode:
streamlit run app.py --logger.level=debug
```

---

## 🔐 Security Considerations

### For Production Use
1. **Enable HTTPS**
   - Use reverse proxy (nginx)
   - Install SSL certificate
   - Redirect HTTP to HTTPS

2. **Add Authentication**
   - Streamlit doesn't have built-in auth
   - Use reverse proxy with authentication
   - Or add auth middleware

3. **Data Protection**
   - Don't store sensitive data in code
   - Use environment variables
   - Encrypt connections

4. **Access Control**
   - Restrict to internal network
   - Use VPN for remote access
   - Implement role-based access

---

## 📞 Support

### Common Issues Checklist
- [ ] Python version 3.8+?
- [ ] Requirements installed? `pip list | grep streamlit`
- [ ] Data files present?
- [ ] Model files present?
- [ ] Port 8501 available?
- [ ] No firewall blocking?

### Getting Help
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Review logs in terminal
3. Try restarting: `Ctrl+C`, then run again
4. Clear cache and restart
5. Check GitHub issues

---

## 📚 Additional Resources

- **Streamlit Documentation**: https://docs.streamlit.io/
- **Python Tutorials**: https://python.org/
- **Dashboard FAQ**: [../README.md](../README.md)

---

## ✅ Deployment Checklist

Before going live:
- [ ] Python 3.8+ installed
- [ ] Requirements installed: `pip list | grep streamlit`
- [ ] Model files verified: `models/*.pkl`
- [ ] Data files verified: `data/processed/*.csv`
- [ ] Dashboard runs locally without errors
- [ ] All sections load correctly
- [ ] Interactions work smoothly
- [ ] Performance acceptable
- [ ] Network access configured
- [ ] Backup plan in place
- [ ] Support team trained
- [ ] Go/no-go decision made

---

## 🎉 You're Ready!

Your AI Price Optima dashboard is ready to deploy and use. 

**Next Steps**:
1. Run the dashboard
2. Test all features
3. Share with team
4. Gather feedback
5. Iterate and improve

```bash
streamlit run app.py
```

**Success!** 🚀

---

*For detailed information about the system, see [FINAL_EVALUATION_REPORT.md](FINAL_EVALUATION_REPORT.md) and [ROLLOUT_PLAN.md](ROLLOUT_PLAN.md)*
