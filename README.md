# Pharmacy Up-Scaling
An end-to-end, locally deployed model and data analytics solution engineered to optimize independent pharmacy operations, automate repetitive workflows, and enhance regulatory compliance. Built entirely with free, open-source tools and a localized Large Language Model (LLM) to ensure strict **data privacy** and zero operational subscription costs.

**Live Dashboard Available:** Built using Streamlit to visualize predictive inventory and batch compliance tracking in real-time.

---

## The Motivation

WHile working for an Independent pharmacy in graduate school, I noticed that Independent pharmacies operate on exceptionally lean teams and tight margins. Valuable hours are often consumed by manual administrative overhead; such as drafting patient communications, auditing expiration dates, labelling, and compiling performance metrics. 

This project serves to demonstrate to healthcare management that modern, privacy-preserving data tools can be deployed **today** using entirely free, local infrastructure, shifting administrative hours back to high-value clinical patient care.

---

## Core Technology Stack

* **Language:** Python
* **Local LLM Infrastructure:** Ollama running **Llama 3.2** (100% offline on my Mac at home, with local execution ensuring no patient data ever leaves the local network)
* **Data Science & Forecasting:** Pandas, NumPy, Statsmodels (Time-Series Forecasting)
* **Interactive UI/Dashboard:** Streamlit

---

##  Functional Architecture (Module Breakdown)

The system is organized into five modular components, each addressing a distinct operational friction point:

### 1. Patient Engagement & Refill Automation
* **Problem:** Manual tracking and outreach for routine clinical follow-ups.
* **Solution:** Automatically parses patient lists, identifies individuals overdue for critical therapeutics (e.g., Vitamin B12 injections), and utilizes the local LLM to instantly generate personalized, clinically appropriate reminder emails.

### 2. Predictive Demand Forecasting
* **Problem:** Inventory stockouts or capital tied up in excess shelf stock.
* **Solution:** Leverages historical sales data to execute a **12-week predictive demand model**. (e.g., Successfully projected a **7.8% increase** in weekly volume, forecasting a rise from 256 units to a peak of 290 units to optimize purchasing pipelines).

### 3. Automated Batch Expiry & Compliance Monitoring
* **Problem:** High-risk manual audits of compounded batch expiration dates.
* **Solution:** Dynamically calculates days remaining for all active compounds. Features a color-coded automated alert system (**Red** = Urgent, **Yellow** = Warning, **Green** = Stable) to eliminate audit vulnerabilities and protect patient safety.

### 4. Smart Staff Scheduling Optimizer
* **Problem:** Scheduling conflicts, compliance overages, and coverage gaps.
* **Solution:** Automatically generates a weekly master schedule based on staff availability matrices, flags contract hour overages, and outputs an AI-generated, plain-English management brief detailing workload balance.

### 5. Executive KPI Report Generator
* **Problem:** Time-intensive consolidation of monthly store performance metrics.
* **Solution:** Aggregates raw monthly administrative data and uses the local LLM to synthesize a polished, executive-ready performance summary in seconds.

---

##  Interactive Web Dashboard

To bridge the gap between backend analytics and end-user operations, a web interface was engineered via **Streamlit**, featuring:
* **Inventory Forecast Page:** Displays interactive historical sales trends side-by-side with the 12-week predictive outlook, complete with statistical confidence intervals.
* **Compliance Control Center:** Visualizes active compound batches alongside a dynamic bar chart tracking days until expiry, embedded with clear warning thresholds at the **3-day** and **7-day** markers.

---
Please feel free to explore. 
Thanks for indulging me, even if my Boss didn't.
##  Live Dashboard
 [Click here to view the live dashboard](https://pharmacy-ai-poc-nzddlxdcetf97qr8lnralv.streamlit.app)
