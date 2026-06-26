# End-to-End Industrial Predictive Maintenance Pipeline

An enterprise-grade predictive maintenance framework that combines statistical process control, high-frequency signal processing, machine learning, and business intelligence to intercept machine failures, protecting a simulated **$305.10M** operational downtime risk.

---

## 📊 1. Financial Baseline & Control Limits (Excel)
Before writing any code, a financial and statistical baseline was established:
* **Financial Risk:** Evaluated 10,000 operational cycles where unexpected mechanical failure creates a $5,000/hr downtime loss (averaging 180 hours per crash), totaling **$305.10M** in operational exposure.
* **Statistical Process Control (SPC):** Calculated historical baseline averages and an Upper Control Limit ($UCL$) using a $+3\sigma$ threshold ($314.44\text{K}$) to define thermal anomalies.

> 💡 *[REPLACE THIS TEXT WITH YOUR EXCEL SCREENSHOT: Drag your Excel screenshot into your repo, name it excel_caps.png, and use this markdown tag to display it: `![Excel Math](excel_caps.png)`]*

---

## 🗄️ 2. Relational Database & Risk Analysis (SQL)
The raw factory dataset was structured and loaded into a relational SQLite database (`factory_vault.db`). 

To isolate high-risk machinery without heavy subquery overhead, a **SQL Common Table Expression (CTE)** was engineered to filter thermal violations and group failure frequencies by machine variant ($L, M, H$):

```sql
WITH Overheating_Alerts AS (
    SELECT Type, Torque, Machine_Failure
    FROM milling_telemetry
    WHERE Process_Temp > 311.0
)
SELECT 
    Type,
    COUNT(*) as Total_Overheat_Events,
    SUM(Machine_Failure) as Actual_Breakdowns,
    ROUND(AVG(Torque), 2) as Avg_Torque_During_Overheat
FROM Overheating_Alerts
GROUP BY Type;