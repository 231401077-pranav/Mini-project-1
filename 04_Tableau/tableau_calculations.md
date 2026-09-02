# Tableau Workbook Calculation & Interactive Dashboard Specification
**Project:** Financial Transaction & Customer Analytics System  
**File:** `Financial_Analytics.twbx`  
**Domain:** Financial Data Analytics  

---

## 1. Tableau Calculated Fields Reference

### Calculated Field 1: Total Revenue
```tableau
SUM([Amount])
```

### Calculated Field 2: Average Transaction Value (ATV)
```tableau
AVG([Amount])
```

### Calculated Field 3: Active Customers Count
```tableau
COUNTD([Customer Id])
```

### Calculated Field 4: Customer Age
```tableau
DATEDIFF('year', [Dob], [Transaction Timestamp])
```

### Calculated Field 5: Customer Age Group Segment
```tableau
IF [Age] < 25 THEN "<25"
ELSEIF [Age] <= 34 THEN "25-34"
ELSEIF [Age] <= 49 THEN "35-49"
ELSEIF [Age] <= 64 THEN "50-64"
ELSE "65+"
END
```

### Calculated Field 6: Risk Status Label
```tableau
IF [Is Fraud] = 1 THEN "Flagged Fraud"
ELSEIF [Amount] >= 1000 THEN "High-Value Transaction"
ELSEIF [Amount] >= 500 AND ([Category] = "shopping_net" OR [Category] = "misc_net") THEN "Suspicious High-Value"
ELSE "Normal"
END
```

### Calculated Field 7: Fraud Rate %
```tableau
SUM(IF [Is Fraud] = 1 THEN 1 ELSE 0 END) / COUNT([Transaction Id]) * 100
```

### Calculated Field 8: Digital vs Card Payment Classification
```tableau
IF [Payment Method Name] IN ("Mobile Wallet", "UPI / Bank Transfer") THEN "Digital Channel"
ELSE "Card / POS Channel"
END
```

---

## 2. Tableau Parameters

1. **`[Top N Customers Parameter]`**: Integer Parameter (Default: 10, Range: 5 to 50) used to dynamically slice Top N customers by lifetime spend.
2. **`[Select Metric Parameter]`**: String List Parameter (`Total Revenue`, `Transaction Volume`, `Average Spend`, `Fraud Exposure`) allowing users to dynamically switch chart measures.
3. **`[Risk Category Filter Parameter]`**: Allows dynamic filtering across `All`, `Flagged Fraud`, `High-Value`, and `Normal`.

---

## 3. Tableau Dashboard Actions & Interactivity

- **Action 1: Category Filter Action**: Clicking a category in the Super-Category Treemap filters Customer Leaderboard, Payment Method bar chart, and Risk distribution.
- **Action 2: State Map Highlight Action**: Hovering/Clicking a state on the US Map highlights corresponding customer transaction records.
- **Action 3: Risk Drill-Down Action**: Clicking the Fraud Risk KPI card filters the transaction audit table to display exact suspicious transactions.
